# -*- coding: utf-8 -*- #
# Copyright 2021 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utilities for the cloud deploy release commands."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import datetime
import os.path
import shutil
import tarfile
import uuid

from apitools.base.py import exceptions as apitools_exceptions
from googlecloudsdk.api_lib.cloudbuild import snapshot
from googlecloudsdk.api_lib.clouddeploy import client_util
from googlecloudsdk.api_lib.clouddeploy import delivery_pipeline
from googlecloudsdk.api_lib.storage import storage_api
from googlecloudsdk.calliope import exceptions as c_exceptions
from googlecloudsdk.command_lib.deploy import exceptions
from googlecloudsdk.command_lib.deploy import rollout_util
from googlecloudsdk.command_lib.deploy import staging_bucket_util
from googlecloudsdk.command_lib.deploy import target_util
from googlecloudsdk.core import log
from googlecloudsdk.core import resources
from googlecloudsdk.core import yaml
from googlecloudsdk.core.resource import resource_transform
from googlecloudsdk.core.util import files
from googlecloudsdk.core.util import times
import six

_RELEASE_COLLECTION = 'clouddeploy.projects.locations.deliveryPipelines.releases'
_ALLOWED_SOURCE_EXT = ['.zip', '.tgz', '.gz']
_SOURCE_STAGING_TEMPLATE = 'gs://{}/source'
RESOURCE_NOT_FOUND = ('The following resources are snapped in the release, '
                      'but no longer exist:\n{}\n\nThese resources were cached '
                      'when the release was created, but their source '
                      'may have been deleted.\n\n')
RESOURCE_CREATED = (
    'The following target is not snapped in the release:\n{}\n\n'
    'You may have specified a target that wasn\'t '
    'cached when the release was created.\n\n')
RESOURCE_CHANGED = ('The following snapped releases resources differ from '
                    'their current definition:\n{}\n\nThe pipeline or targets '
                    'were cached when the release was created, but the source '
                    'has changed since then. You should review the differences '
                    'before proceeding.\n')
_DATE_PATTERN = '$DATE'
_TIME_PATTERN = '$TIME'
GENERATED_SKAFFOLD_TEMPLATE = """\
apiVersion: skaffold/v2beta28
kind: Config
deploy:
  kubectl:
    manifests:
      - {}
  """
GENERATED_SKAFFOLD = 'skaffold.yaml'


def RenderPattern(release_id):
  """Finds and replaces keywords in the release name.

    When adding to the list of keywords that can be expanded, care must be taken
    when two words share the same prefix ie. ($D and $DATE). In that case the
    longer keyword ($DATE) must be processed before the shorter one ($D).
  Args:
    release_id: str, the release name template.

  Returns:
    The formatted release name
  """
  time_now = datetime.datetime.utcnow()
  formatted_id = release_id.replace(_DATE_PATTERN, time_now.strftime('%Y%m%d'))
  formatted_id = formatted_id.replace(_TIME_PATTERN, time_now.strftime('%H%M'))
  _CheckForRemainingDollars(formatted_id)
  return formatted_id


def _CheckForRemainingDollars(release_id):
  """Find and notify user about dollar signs in release name."""

  dollar_positions = []
  for i in range(len(release_id)):
    if release_id[i] == '$':
      dollar_positions.append(six.text_type(i))
  if dollar_positions:
    raise exceptions.InvalidReleaseNameError(release_id, dollar_positions)


def SetBuildArtifacts(images, messages, release_config):
  """Set build_artifacts field of the release message.

  Args:
    images: dict[str,dict], docker image name and tag dictionary.
    messages: Module containing the Cloud Deploy messages.
    release_config: apitools.base.protorpclite.messages.Message, Cloud Deploy
      release message.

  Returns:
    Cloud Deploy release message.
  """
  if not images:
    return release_config
  build_artifacts = []
  for key, value in sorted(six.iteritems(images)):  # Sort for tests
    build_artifacts.append(messages.BuildArtifact(image=key, tag=value))
  release_config.buildArtifacts = build_artifacts

  return release_config


def LoadBuildArtifactFile(path):
  """Load images from a file containing JSON build data.

  Args:
    path: str, build artifacts file path.

  Returns:
    Docker image name and tag dictionary.
  """
  with files.FileReader(path) as f:  # Returns user-friendly error messages
    try:
      structured_data = yaml.load(f, file_hint=path)
    except yaml.Error as e:
      raise exceptions.ParserError(path, e.inner_error)
    images = {}
    for build in structured_data['builds']:
      # For b/191063894. Supporting both name for now.
      images[build.get('image', build.get('imageName'))] = build['tag']

    return images


def CreateReleaseConfig(source,
                        gcs_source_staging_dir,
                        ignore_file,
                        images,
                        build_artifacts,
                        description,
                        skaffold_version,
                        skaffold_file,
                        location,
                        pipeline_uuid,
                        from_k8s_manifest,
                        hide_logs=False):
  """Returns a build config."""

  # If the kubernetes manifest was given, this means a Skaffold file should be
  # generated, so we should not check at this stage if the Skaffold file exists.
  if not from_k8s_manifest:
    _VerifySkaffoldFileExists(source, skaffold_file)
  messages = client_util.GetMessagesModule(client_util.GetClientInstance())
  release_config = messages.Release()
  release_config.description = description
  release_config = _SetSource(
      release_config,
      source,
      gcs_source_staging_dir,
      ignore_file,
      skaffold_version,
      location,
      pipeline_uuid,
      from_k8s_manifest,
      skaffold_file,
      hide_logs,
  )
  release_config = _SetImages(messages, release_config, images, build_artifacts)
  return release_config


def _CreateAndUploadTarball(gcs_client,
                            gcs_source_staging,
                            source,
                            ignore_file,
                            hide_logs,
                            release_config,
                            print_skaffold_config=False):
  """Creates a local tarball and uploads it to GCS.

     After creating and uploading the tarball, this sets the Skaffold config URI
     in the release config.

  Args:
    gcs_client: client for Google Cloud Storage API.
    gcs_source_staging: directory in Google cloud storage to use for staging
    source: the location of the source files
    ignore_file: the ignore file to use
    hide_logs: whether to show logs, defaults to False
    release_config: release configuration
    print_skaffold_config: if true, the Cloud Storage URI of tar.gz archive
      containing Skaffold configuration will be printed, defaults to False.
  """
  source_snapshot = snapshot.Snapshot(source, ignore_file=ignore_file)
  size_str = resource_transform.TransformSize(source_snapshot.uncompressed_size)
  if not hide_logs:
    log.status.Print('Creating temporary tarball archive of {num_files} file(s)'
                     ' totalling {size} before compression.'.format(
                         num_files=len(source_snapshot.files), size=size_str))
  # This makes a tarball of the snapshot and then copies to GCS.
  staged_source_obj = source_snapshot.CopyTarballToGCS(
      gcs_client,
      gcs_source_staging,
      ignore_file=ignore_file,
      hide_logs=hide_logs)
  release_config.skaffoldConfigUri = 'gs://{bucket}/{object}'.format(
      bucket=staged_source_obj.bucket, object=staged_source_obj.name)
  if print_skaffold_config:
    log.status.Print(
        'Generated Skaffold file can be found here: {config_uri}'.format(
            config_uri=release_config.skaffoldConfigUri,))


def _SetSource(release_config,
               source,
               gcs_source_staging_dir,
               ignore_file,
               skaffold_version,
               location,
               pipeline_uuid,
               kubernetes_manifest,
               skaffold_file,
               hide_logs=False):
  """Set the source for the release config.

  Sets the source for the release config and creates a default Cloud Storage
  bucket with location for staging if gcs-source-staging-dir is not specified.

  Args:
    release_config: a Release message
    source: the location of the source files
    gcs_source_staging_dir: directory in google cloud storage to use for staging
    ignore_file: the ignore file to use
    skaffold_version: version of Skaffold binary
    location: the cloud region for the release
    pipeline_uuid: the unique id of the release's parent pipeline.
    kubernetes_manifest: path to kubernetes manifest (e.g. /home/user/k8.yaml).
      If provided, a Skaffold file will be generated and uploaded to GCS on
      behalf of the customer.
    skaffold_file: path of the skaffold file relative to the source directory
      that contains the Skaffold file.
    hide_logs: whether to show logs, defaults to False

  Returns:
    Modified release_config
  """
  default_gcs_source = False
  default_bucket_name = staging_bucket_util.GetDefaultStagingBucket(
      pipeline_uuid)

  if gcs_source_staging_dir is None:
    default_gcs_source = True
    gcs_source_staging_dir = _SOURCE_STAGING_TEMPLATE.format(
        default_bucket_name)

  if not gcs_source_staging_dir.startswith('gs://'):
    raise c_exceptions.InvalidArgumentException(
        parameter_name='--gcs-source-staging-dir',
        message=gcs_source_staging_dir)

  gcs_client = storage_api.StorageClient()
  suffix = '.tgz'
  if source.startswith('gs://') or os.path.isfile(source):
    _, suffix = os.path.splitext(source)

  # Next, stage the source to Cloud Storage.
  staged_object = '{stamp}-{uuid}{suffix}'.format(
      stamp=times.GetTimeStampFromDateTime(times.Now()),
      uuid=uuid.uuid4().hex,
      suffix=suffix,
  )
  gcs_source_staging_dir = resources.REGISTRY.Parse(
      gcs_source_staging_dir, collection='storage.objects')

  try:
    gcs_client.CreateBucketIfNotExists(
        gcs_source_staging_dir.bucket,
        location=location,
        check_ownership=default_gcs_source)
  except storage_api.BucketInWrongProjectError:
    # If we're using the default bucket but it already exists in a different
    # project, then it could belong to a malicious attacker (b/33046325).
    raise c_exceptions.RequiredArgumentException(
        'gcs-source-staging-dir',
        'A bucket with name {} already exists and is owned by '
        'another project. Specify a bucket using '
        '--gcs-source-staging-dir.'.format(default_bucket_name))

  if gcs_source_staging_dir.object:
    staged_object = gcs_source_staging_dir.object + '/' + staged_object
  gcs_source_staging = resources.REGISTRY.Create(
      collection='storage.objects',
      bucket=gcs_source_staging_dir.bucket,
      object=staged_object)
  if source.startswith('gs://'):
    gcs_source = resources.REGISTRY.Parse(source, collection='storage.objects')
    staged_source_obj = gcs_client.Rewrite(gcs_source, gcs_source_staging)
    release_config.skaffoldConfigUri = 'gs://{bucket}/{object}'.format(
        bucket=staged_source_obj.bucket, object=staged_source_obj.name)
  else:
    # If a Skaffold file should be generated
    if kubernetes_manifest:
      _UploadTarballGeneratedSkaffoldAndK8(kubernetes_manifest, gcs_client,
                                           gcs_source_staging, ignore_file,
                                           hide_logs, release_config)
    elif os.path.isdir(source):
      _CreateAndUploadTarball(gcs_client, gcs_source_staging, source,
                              ignore_file, hide_logs, release_config)
    # When its a tar file
    elif os.path.isfile(source):
      if not hide_logs:
        log.status.Print('Uploading local file [{src}] to '
                         '[gs://{bucket}/{object}].'.format(
                             src=source,
                             bucket=gcs_source_staging.bucket,
                             object=gcs_source_staging.object,
                         ))
      staged_source_obj = gcs_client.CopyFileToGCS(source, gcs_source_staging)
      release_config.skaffoldConfigUri = 'gs://{bucket}/{object}'.format(
          bucket=staged_source_obj.bucket, object=staged_source_obj.name)

  if skaffold_version:
    release_config.skaffoldVersion = skaffold_version

  release_config = _SetSkaffoldConfigPath(release_config, skaffold_file,
                                          kubernetes_manifest)

  return release_config


def _UploadTarballGeneratedSkaffoldAndK8(kubernetes_manifest, gcs_client,
                                         gcs_source_staging, ignore_file,
                                         hide_logs, release_config):
  """Generates a Skaffold file and uploads the file and k8 manifest to GCS.

  Args:
    kubernetes_manifest: path to kubernetes manifest (e.g. /home/user/k8.yaml).
      If provided, a Skaffold file will be generated and uploaded to GCS on
      behalf of the customer.
    gcs_client: client for Google Cloud Storage API.
    gcs_source_staging: directory in google cloud storage to use for staging
    ignore_file: the ignore file to use
    hide_logs: whether to show logs, defaults to False
    release_config: a Release message
  """
  # Check that the kubernetes file exists.
  if not os.path.exists(kubernetes_manifest):
    raise c_exceptions.BadFileException(
        'could not find kubernetes file [{src}]'.format(
            src=kubernetes_manifest))
  # Create the YAML data. Copying to a temp directory to avoid editing
  # the local directory.
  k8_file_name = os.path.basename(kubernetes_manifest)
  skaffold_yaml = yaml.load(GENERATED_SKAFFOLD_TEMPLATE.format(k8_file_name))
  with files.TemporaryDirectory() as temp_dir:
    skaffold_path = os.path.join(temp_dir, GENERATED_SKAFFOLD)
    # Copy the kubernetes file to the temp directory
    shutil.copy(kubernetes_manifest, temp_dir)
    with files.FileWriter(skaffold_path) as f:
      # Dump the yaml data to the Skaffold file
      yaml.dump(skaffold_yaml, f)
      _CreateAndUploadTarball(gcs_client, gcs_source_staging, temp_dir,
                              ignore_file, hide_logs, release_config, True)


def _VerifySkaffoldFileExists(source, skaffold_file):
  """Checks that the specified source contains a skaffold configuration file."""
  if not skaffold_file:
    skaffold_file = 'skaffold.yaml'
  if source.startswith('gs://'):
    log.status.Print(
        'Skipping skaffold file check. Reason: source is not a local archive or directory'
    )
  elif not os.path.exists(source):
    raise c_exceptions.BadFileException(
        'could not find source [{src}]'.format(src=source))
  elif os.path.isfile(source):
    _VerifySkaffoldIsInArchive(source, skaffold_file)
  else:
    _VerifySkaffoldIsInFolder(source, skaffold_file)


def _VerifySkaffoldIsInArchive(source, skaffold_file):
  """Checks that the specified source file is a readable archive with skaffold file present."""
  _, ext = os.path.splitext(source)
  if ext not in _ALLOWED_SOURCE_EXT:
    raise c_exceptions.BadFileException('local file [{src}] is none of ' +
                                        ', '.join(_ALLOWED_SOURCE_EXT))
  if not tarfile.is_tarfile(source):
    raise c_exceptions.BadFileException(
        'Specified source file is not a readable compressed file archive')
  with tarfile.open(source, mode='r:gz') as archive:
    try:
      archive.getmember(skaffold_file)
    except KeyError:
      raise c_exceptions.BadFileException(
          'Could not find skaffold file. File [{skaffold}] does not exist in source archive'
          .format(skaffold=skaffold_file))


def _VerifySkaffoldIsInFolder(source, skaffold_file):
  """Checks that the specified source folder contains a skaffold configuration file."""
  path_to_skaffold = os.path.join(source, skaffold_file)
  if not os.path.exists(path_to_skaffold):
    raise c_exceptions.BadFileException(
        'Could not find skaffold file. File [{skaffold}] does not exist'.format(
            skaffold=path_to_skaffold))


def _SetImages(messages, release_config, images, build_artifacts):
  """Set the image substitutions for the release config."""
  if build_artifacts:
    images = LoadBuildArtifactFile(build_artifacts)

  return SetBuildArtifacts(images, messages, release_config)


def _SetSkaffoldConfigPath(release_config, skaffold_file, kubernetes_manifest):
  """Set the path for skaffold configuration file relative to source directory."""
  if skaffold_file:
    release_config.skaffoldConfigPath = skaffold_file
  if kubernetes_manifest:
    release_config.skaffoldConfigPath = GENERATED_SKAFFOLD

  return release_config


def ListCurrentDeployedTargets(release_ref, targets):
  """Lists the targets where the given release is the latest.

  Args:
    release_ref: protorpc.messages.Message, protorpc.messages.Message, release
      reference.
    targets: protorpc.messages.Message, protorpc.messages.Message, list of
      target objects.

  Returns:
    A list of target references where this release is deployed.
  """
  matching_targets = []
  release_name = release_ref.RelativeName()
  pipeline_ref = release_ref.Parent()
  for obj in targets:
    target_name = obj.name
    target_ref = target_util.TargetReferenceFromName(target_name)
    # Gets the latest rollout of this target
    rollout_obj = target_util.GetCurrentRollout(target_ref, pipeline_ref)
    if rollout_obj is None:
      continue
    rollout_ref = rollout_util.RolloutReferenceFromName(rollout_obj.name)
    deployed_release_name = rollout_ref.Parent().RelativeName()
    if release_name == deployed_release_name:
      matching_targets.append(target_ref)
  return matching_targets


def DiffSnappedPipeline(release_ref, release_obj, to_target=None):
  """Detects the differences between current delivery pipeline and target definitions, from those associated with the release being promoted.

  Changes are determined through etag value differences.

  This runs the following checks:
    - if the to_target is one of the snapped targets in the release.
    - if the snapped targets still exist.
    - if the snapped targets have been changed.
    - if the snapped pipeline still exists.
    - if the snapped pipeline has been changed.

  Args:
    release_ref: protorpc.messages.Message, release resource object.
    release_obj: apitools.base.protorpclite.messages.Message, release message.
    to_target: str, the target to promote the release to. If specified, this
      verifies if the target has been snapped in the release.

  Returns:
    the list of the resources that no longer exist.
    the list of the resources that have been changed.
    the list of the resources that aren't snapped in the release.
  """
  resource_not_found = []
  resource_changed = []
  resource_created = []
  # check if the to_target is one of the snapped targets in the release.
  if to_target:
    ref_dict = release_ref.AsDict()
    # Creates shared target by default.
    target_ref = target_util.TargetReference(
        to_target,
        ref_dict['projectsId'],
        ref_dict['locationsId'],
    )
    # Only compare the resource ID, for the case that
    # if release_ref is parsed from arguments, it will use project ID,
    # whereas, the project number is stored in the DB.

    if target_ref.Name() not in [
        target_util.TargetId(obj.name) for obj in release_obj.targetSnapshots
    ]:
      resource_created.append(target_ref.RelativeName())

  for obj in release_obj.targetSnapshots:
    target_name = obj.name
    # Check if the snapped targets still exist.
    try:
      target_obj = target_util.GetTarget(
          target_util.TargetReferenceFromName(target_name))
      # Checks if the snapped targets have been changed.
      if target_obj.etag != obj.etag:
        resource_changed.append(target_name)
    except apitools_exceptions.HttpError as error:
      log.debug('Failed to get target {}: {}'.format(target_name, error))
      log.status.Print('Unable to get target {}\n'.format(target_name))
      resource_not_found.append(target_name)

  name = release_obj.deliveryPipelineSnapshot.name
  # Checks if the pipeline exists.
  try:
    pipeline_obj = delivery_pipeline.DeliveryPipelinesClient().Get(name)
    # Checks if the pipeline has been changed.
    if pipeline_obj.etag != release_obj.deliveryPipelineSnapshot.etag:
      resource_changed.append(release_ref.Parent().RelativeName())
  except apitools_exceptions.HttpError as error:
    log.debug('Failed to get pipeline {}: {}'.format(name, error.content))
    log.status.Print('Unable to get delivery pipeline {}'.format(name))
    resource_not_found.append(name)

  return resource_created, resource_changed, resource_not_found


def PrintDiff(release_ref, release_obj, target_id=None, prompt=''):
  """Prints differences between current and snapped delivery pipeline and target definitions.

  Args:
    release_ref: protorpc.messages.Message, release resource object.
    release_obj: apitools.base.protorpclite.messages.Message, release message.
    target_id: str, target id, e.g. test/stage/prod.
    prompt: str, prompt text.
  """
  resource_created, resource_changed, resource_not_found = DiffSnappedPipeline(
      release_ref, release_obj, target_id)

  if resource_created:
    prompt += RESOURCE_CREATED.format('\n'.join(BulletedList(resource_created)))
  if resource_not_found:
    prompt += RESOURCE_NOT_FOUND.format('\n'.join(
        BulletedList(resource_not_found)))
  if resource_changed:
    prompt += RESOURCE_CHANGED.format('\n'.join(BulletedList(resource_changed)))

  log.status.Print(prompt)


def BulletedList(str_list):
  """Converts a list of string to a bulleted list.

  The returned list looks like ['- string1','- string2'].

  Args:
    str_list: [str], list to be converted.

  Returns:
    list of the transformed strings.
  """
  for i in range(len(str_list)):
    str_list[i] = '- ' + str_list[i]

  return str_list


def GetSnappedTarget(release_obj, target_id):
  """Get the snapped target in a release by target ID.

  Args:
    release_obj: apitools.base.protorpclite.messages.Message, release message
      object.
    target_id: str, target ID.

  Returns:
    target message object.
  """
  target_obj = None

  for ss in release_obj.targetSnapshots:
    if target_util.TargetId(ss.name) == target_id:
      target_obj = ss
      break

  return target_obj
