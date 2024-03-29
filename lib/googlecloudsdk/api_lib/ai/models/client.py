# -*- coding: utf-8 -*- #
# Copyright 2020 Google LLC. All Rights Reserved.
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
"""Utilities for AI Platform models API."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from apitools.base.py import list_pager
from googlecloudsdk.api_lib.util import apis
from googlecloudsdk.command_lib.ai import constants


class ModelsClient(object):
  """High-level client for the AI Platform models surface."""

  def __init__(self, client=None, messages=None):
    self.client = client or apis.GetClientInstance(
        constants.AI_PLATFORM_API_NAME,
        constants.AI_PLATFORM_API_VERSION[constants.BETA_VERSION])
    self.messages = messages or self.client.MESSAGES_MODULE
    self._service = self.client.projects_locations_models

  def UploadV1Beta1(self,
                    region_ref=None,
                    display_name=None,
                    description=None,
                    artifact_uri=None,
                    container_image_uri=None,
                    container_command=None,
                    container_args=None,
                    container_env_vars=None,
                    container_ports=None,
                    container_predict_route=None,
                    container_health_route=None,
                    explanation_spec=None,
                    parent_model=None,
                    model_id=None,
                    version_aliases=None):
    """Constructs, sends an UploadModel request and returns the LRO to be done."""
    container_spec = self.messages.GoogleCloudAiplatformV1beta1ModelContainerSpec(
        healthRoute=container_health_route,
        imageUri=container_image_uri,
        predictRoute=container_predict_route)
    if container_command:
      container_spec.command = container_command
    if container_args:
      container_spec.args = container_args
    if container_env_vars:
      container_spec.env = [
          self.messages.GoogleCloudAiplatformV1beta1EnvVar(
              name=k, value=container_env_vars[k]) for k in container_env_vars
      ]
    if container_ports:
      container_spec.ports = [
          self.messages.GoogleCloudAiplatformV1beta1Port(containerPort=port)
          for port in container_ports
      ]

    model = self.messages.GoogleCloudAiplatformV1beta1Model(
        artifactUri=artifact_uri,
        containerSpec=container_spec,
        description=description,
        displayName=display_name,
        explanationSpec=explanation_spec)
    if version_aliases:
      model.versionAliases = version_aliases

    return self._service.Upload(
        self.messages.AiplatformProjectsLocationsModelsUploadRequest(
            parent=region_ref.RelativeName(),
            googleCloudAiplatformV1beta1UploadModelRequest=self.messages
            .GoogleCloudAiplatformV1beta1UploadModelRequest(
                model=model,
                parentModel=parent_model,
                modelId=model_id)))

  def UploadV1(self,
               region_ref=None,
               display_name=None,
               description=None,
               artifact_uri=None,
               container_image_uri=None,
               container_command=None,
               container_args=None,
               container_env_vars=None,
               container_ports=None,
               container_predict_route=None,
               container_health_route=None,
               explanation_spec=None,
               parent_model=None,
               model_id=None,
               version_aliases=None):
    """Constructs, sends an UploadModel request and returns the LRO to be done."""
    container_spec = self.messages.GoogleCloudAiplatformV1ModelContainerSpec(
        healthRoute=container_health_route,
        imageUri=container_image_uri,
        predictRoute=container_predict_route)
    if container_command:
      container_spec.command = container_command
    if container_args:
      container_spec.args = container_args
    if container_env_vars:
      container_spec.env = [
          self.messages.GoogleCloudAiplatformV1EnvVar(
              name=k, value=container_env_vars[k]) for k in container_env_vars
      ]
    if container_ports:
      container_spec.ports = [
          self.messages.GoogleCloudAiplatformV1Port(containerPort=port)
          for port in container_ports
      ]

    model = self.messages.GoogleCloudAiplatformV1Model(
        artifactUri=artifact_uri,
        containerSpec=container_spec,
        description=description,
        displayName=display_name,
        explanationSpec=explanation_spec)
    if version_aliases:
      model.versionAliases = version_aliases

    return self._service.Upload(
        self.messages.AiplatformProjectsLocationsModelsUploadRequest(
            parent=region_ref.RelativeName(),
            googleCloudAiplatformV1UploadModelRequest=self.messages
            .GoogleCloudAiplatformV1UploadModelRequest(
                model=model,
                parentModel=parent_model,
                modelId=model_id)))

  def Get(self, model_ref):
    request = self.messages.AiplatformProjectsLocationsModelsGetRequest(
        name=model_ref.RelativeName())
    return self._service.Get(request)

  def Delete(self, model_ref):
    request = self.messages.AiplatformProjectsLocationsModelsDeleteRequest(
        name=model_ref.RelativeName())
    return self._service.Delete(request)

  def DeleteVersion(self, model_version_ref):
    """Deletes the given model version.

    Args:
      model_version_ref: The resource reference for a given model version.

    Returns:
      Response from calling delete version with request containing given model
      version.
    """
    request = self.messages.AiplatformProjectsLocationsModelsDeleteVersionRequest(
        name=model_version_ref.RelativeName())
    return self._service.DeleteVersion(request)

  def List(self, limit=None, region_ref=None):
    return list_pager.YieldFromList(
        self._service,
        self.messages.AiplatformProjectsLocationsModelsListRequest(
            parent=region_ref.RelativeName()),
        field='models',
        batch_size_attribute='pageSize',
        limit=limit)

  def ListVersion(self, model_ref=None, limit=None):
    """List all model versions of the given model.

    Args:
      model_ref: The resource reference for a given model. None if model
        resource reference is not provided.
      limit: int, The maximum number of records to yield. None if all available
        records should be yielded.

    Returns:
      Response from calling list model versions with request containing given
      model and limit.
    """
    return list_pager.YieldFromList(
        self._service,
        self.messages.AiplatformProjectsLocationsModelsListVersionsRequest(
            name=model_ref.RelativeName()),
        method='ListVersions',
        field='models',
        batch_size_attribute='pageSize',
        limit=limit)
