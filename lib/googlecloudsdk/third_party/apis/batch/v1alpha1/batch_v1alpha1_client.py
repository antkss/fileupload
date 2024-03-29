"""Generated client library for batch version v1alpha1."""
# NOTE: This file is autogenerated and should not be edited by hand.

from __future__ import absolute_import

from apitools.base.py import base_api
from googlecloudsdk.third_party.apis.batch.v1alpha1 import batch_v1alpha1_messages as messages


class BatchV1alpha1(base_api.BaseApiClient):
  """Generated client library for service batch version v1alpha1."""

  MESSAGES_MODULE = messages
  BASE_URL = 'https://batch.googleapis.com/'
  MTLS_BASE_URL = 'https://batch.mtls.googleapis.com/'

  _PACKAGE = 'batch'
  _SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
  _VERSION = 'v1alpha1'
  _CLIENT_ID = '1042881264118.apps.googleusercontent.com'
  _CLIENT_SECRET = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _USER_AGENT = 'google-cloud-sdk'
  _CLIENT_CLASS_NAME = 'BatchV1alpha1'
  _URL_VERSION = 'v1alpha1'
  _API_KEY = None

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None, response_encoding=None):
    """Create a new batch handle."""
    url = url or self.BASE_URL
    super(BatchV1alpha1, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params,
        additional_http_headers=additional_http_headers,
        response_encoding=response_encoding)
    self.projects_locations_jobs = self.ProjectsLocationsJobsService(self)
    self.projects_locations_nodes = self.ProjectsLocationsNodesService(self)
    self.projects_locations_operations = self.ProjectsLocationsOperationsService(self)
    self.projects_locations_tasks = self.ProjectsLocationsTasksService(self)
    self.projects_locations = self.ProjectsLocationsService(self)
    self.projects = self.ProjectsService(self)

  class ProjectsLocationsJobsService(base_api.BaseApiService):
    """Service class for the projects_locations_jobs resource."""

    _NAME = 'projects_locations_jobs'

    def __init__(self, client):
      super(BatchV1alpha1.ProjectsLocationsJobsService, self).__init__(client)
      self._upload_configs = {
          }

    def GetIamPolicy(self, request, global_params=None):
      r"""Gets the access control policy for a resource. Returns an empty policy if the resource exists and does not have a policy set.

      Args:
        request: (BatchProjectsLocationsJobsGetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Policy) The response message.
      """
      config = self.GetMethodConfig('GetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    GetIamPolicy.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/jobs/{jobsId}:getIamPolicy',
        http_method='GET',
        method_id='batch.projects.locations.jobs.getIamPolicy',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=['options_requestedPolicyVersion'],
        relative_path='v1alpha1/{+resource}:getIamPolicy',
        request_field='',
        request_type_name='BatchProjectsLocationsJobsGetIamPolicyRequest',
        response_type_name='Policy',
        supports_download=False,
    )

    def SetIamPolicy(self, request, global_params=None):
      r"""Sets the access control policy on the specified resource. Replaces any existing policy. Can return `NOT_FOUND`, `INVALID_ARGUMENT`, and `PERMISSION_DENIED` errors.

      Args:
        request: (BatchProjectsLocationsJobsSetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Policy) The response message.
      """
      config = self.GetMethodConfig('SetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    SetIamPolicy.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/jobs/{jobsId}:setIamPolicy',
        http_method='POST',
        method_id='batch.projects.locations.jobs.setIamPolicy',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=[],
        relative_path='v1alpha1/{+resource}:setIamPolicy',
        request_field='setIamPolicyRequest',
        request_type_name='BatchProjectsLocationsJobsSetIamPolicyRequest',
        response_type_name='Policy',
        supports_download=False,
    )

    def TestIamPermissions(self, request, global_params=None):
      r"""Returns permissions that a caller has on the specified resource. If the resource does not exist, this will return an empty set of permissions, not a `NOT_FOUND` error. Note: This operation is designed to be used for building permission-aware UIs and command-line tools, not for authorization checking. This operation may "fail open" without warning.

      Args:
        request: (BatchProjectsLocationsJobsTestIamPermissionsRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (TestIamPermissionsResponse) The response message.
      """
      config = self.GetMethodConfig('TestIamPermissions')
      return self._RunMethod(
          config, request, global_params=global_params)

    TestIamPermissions.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/jobs/{jobsId}:testIamPermissions',
        http_method='POST',
        method_id='batch.projects.locations.jobs.testIamPermissions',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=[],
        relative_path='v1alpha1/{+resource}:testIamPermissions',
        request_field='testIamPermissionsRequest',
        request_type_name='BatchProjectsLocationsJobsTestIamPermissionsRequest',
        response_type_name='TestIamPermissionsResponse',
        supports_download=False,
    )

  class ProjectsLocationsNodesService(base_api.BaseApiService):
    """Service class for the projects_locations_nodes resource."""

    _NAME = 'projects_locations_nodes'

    def __init__(self, client):
      super(BatchV1alpha1.ProjectsLocationsNodesService, self).__init__(client)
      self._upload_configs = {
          }

    def GetIamPolicy(self, request, global_params=None):
      r"""Gets the access control policy for a resource. Returns an empty policy if the resource exists and does not have a policy set.

      Args:
        request: (BatchProjectsLocationsNodesGetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Policy) The response message.
      """
      config = self.GetMethodConfig('GetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    GetIamPolicy.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/nodes/{nodesId}:getIamPolicy',
        http_method='GET',
        method_id='batch.projects.locations.nodes.getIamPolicy',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=['options_requestedPolicyVersion'],
        relative_path='v1alpha1/{+resource}:getIamPolicy',
        request_field='',
        request_type_name='BatchProjectsLocationsNodesGetIamPolicyRequest',
        response_type_name='Policy',
        supports_download=False,
    )

    def SetIamPolicy(self, request, global_params=None):
      r"""Sets the access control policy on the specified resource. Replaces any existing policy. Can return `NOT_FOUND`, `INVALID_ARGUMENT`, and `PERMISSION_DENIED` errors.

      Args:
        request: (BatchProjectsLocationsNodesSetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Policy) The response message.
      """
      config = self.GetMethodConfig('SetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    SetIamPolicy.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/nodes/{nodesId}:setIamPolicy',
        http_method='POST',
        method_id='batch.projects.locations.nodes.setIamPolicy',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=[],
        relative_path='v1alpha1/{+resource}:setIamPolicy',
        request_field='setIamPolicyRequest',
        request_type_name='BatchProjectsLocationsNodesSetIamPolicyRequest',
        response_type_name='Policy',
        supports_download=False,
    )

    def TestIamPermissions(self, request, global_params=None):
      r"""Returns permissions that a caller has on the specified resource. If the resource does not exist, this will return an empty set of permissions, not a `NOT_FOUND` error. Note: This operation is designed to be used for building permission-aware UIs and command-line tools, not for authorization checking. This operation may "fail open" without warning.

      Args:
        request: (BatchProjectsLocationsNodesTestIamPermissionsRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (TestIamPermissionsResponse) The response message.
      """
      config = self.GetMethodConfig('TestIamPermissions')
      return self._RunMethod(
          config, request, global_params=global_params)

    TestIamPermissions.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/nodes/{nodesId}:testIamPermissions',
        http_method='POST',
        method_id='batch.projects.locations.nodes.testIamPermissions',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=[],
        relative_path='v1alpha1/{+resource}:testIamPermissions',
        request_field='testIamPermissionsRequest',
        request_type_name='BatchProjectsLocationsNodesTestIamPermissionsRequest',
        response_type_name='TestIamPermissionsResponse',
        supports_download=False,
    )

  class ProjectsLocationsOperationsService(base_api.BaseApiService):
    """Service class for the projects_locations_operations resource."""

    _NAME = 'projects_locations_operations'

    def __init__(self, client):
      super(BatchV1alpha1.ProjectsLocationsOperationsService, self).__init__(client)
      self._upload_configs = {
          }

    def Cancel(self, request, global_params=None):
      r"""Starts asynchronous cancellation on a long-running operation. The server makes a best effort to cancel the operation, but success is not guaranteed. If the server doesn't support this method, it returns `google.rpc.Code.UNIMPLEMENTED`. Clients can use Operations.GetOperation or other methods to check whether the cancellation succeeded or whether the operation completed despite cancellation. On successful cancellation, the operation is not deleted; instead, it becomes an operation with an Operation.error value with a google.rpc.Status.code of 1, corresponding to `Code.CANCELLED`.

      Args:
        request: (BatchProjectsLocationsOperationsCancelRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('Cancel')
      return self._RunMethod(
          config, request, global_params=global_params)

    Cancel.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/operations/{operationsId}:cancel',
        http_method='POST',
        method_id='batch.projects.locations.operations.cancel',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1alpha1/{+name}:cancel',
        request_field='cancelOperationRequest',
        request_type_name='BatchProjectsLocationsOperationsCancelRequest',
        response_type_name='Empty',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      r"""Deletes a long-running operation. This method indicates that the client is no longer interested in the operation result. It does not cancel the operation. If the server doesn't support this method, it returns `google.rpc.Code.UNIMPLEMENTED`.

      Args:
        request: (BatchProjectsLocationsOperationsDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/operations/{operationsId}',
        http_method='DELETE',
        method_id='batch.projects.locations.operations.delete',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1alpha1/{+name}',
        request_field='',
        request_type_name='BatchProjectsLocationsOperationsDeleteRequest',
        response_type_name='Empty',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets the latest state of a long-running operation. Clients can use this method to poll the operation result at intervals as recommended by the API service.

      Args:
        request: (BatchProjectsLocationsOperationsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/operations/{operationsId}',
        http_method='GET',
        method_id='batch.projects.locations.operations.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1alpha1/{+name}',
        request_field='',
        request_type_name='BatchProjectsLocationsOperationsGetRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists operations that match the specified filter in the request. If the server doesn't support this method, it returns `UNIMPLEMENTED`. NOTE: the `name` binding allows API services to override the binding to use different resource name schemes, such as `users/*/operations`. To override the binding, API services can add a binding such as `"/v1/{name=users/*}/operations"` to their service configuration. For backwards compatibility, the default name includes the operations collection id, however overriding users must ensure the name binding is the parent resource, without the operations collection id.

      Args:
        request: (BatchProjectsLocationsOperationsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListOperationsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/operations',
        http_method='GET',
        method_id='batch.projects.locations.operations.list',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['filter', 'pageSize', 'pageToken'],
        relative_path='v1alpha1/{+name}/operations',
        request_field='',
        request_type_name='BatchProjectsLocationsOperationsListRequest',
        response_type_name='ListOperationsResponse',
        supports_download=False,
    )

  class ProjectsLocationsTasksService(base_api.BaseApiService):
    """Service class for the projects_locations_tasks resource."""

    _NAME = 'projects_locations_tasks'

    def __init__(self, client):
      super(BatchV1alpha1.ProjectsLocationsTasksService, self).__init__(client)
      self._upload_configs = {
          }

    def GetIamPolicy(self, request, global_params=None):
      r"""Gets the access control policy for a resource. Returns an empty policy if the resource exists and does not have a policy set.

      Args:
        request: (BatchProjectsLocationsTasksGetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Policy) The response message.
      """
      config = self.GetMethodConfig('GetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    GetIamPolicy.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/tasks/{tasksId}:getIamPolicy',
        http_method='GET',
        method_id='batch.projects.locations.tasks.getIamPolicy',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=['options_requestedPolicyVersion'],
        relative_path='v1alpha1/{+resource}:getIamPolicy',
        request_field='',
        request_type_name='BatchProjectsLocationsTasksGetIamPolicyRequest',
        response_type_name='Policy',
        supports_download=False,
    )

    def SetIamPolicy(self, request, global_params=None):
      r"""Sets the access control policy on the specified resource. Replaces any existing policy. Can return `NOT_FOUND`, `INVALID_ARGUMENT`, and `PERMISSION_DENIED` errors.

      Args:
        request: (BatchProjectsLocationsTasksSetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Policy) The response message.
      """
      config = self.GetMethodConfig('SetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    SetIamPolicy.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/tasks/{tasksId}:setIamPolicy',
        http_method='POST',
        method_id='batch.projects.locations.tasks.setIamPolicy',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=[],
        relative_path='v1alpha1/{+resource}:setIamPolicy',
        request_field='setIamPolicyRequest',
        request_type_name='BatchProjectsLocationsTasksSetIamPolicyRequest',
        response_type_name='Policy',
        supports_download=False,
    )

    def TestIamPermissions(self, request, global_params=None):
      r"""Returns permissions that a caller has on the specified resource. If the resource does not exist, this will return an empty set of permissions, not a `NOT_FOUND` error. Note: This operation is designed to be used for building permission-aware UIs and command-line tools, not for authorization checking. This operation may "fail open" without warning.

      Args:
        request: (BatchProjectsLocationsTasksTestIamPermissionsRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (TestIamPermissionsResponse) The response message.
      """
      config = self.GetMethodConfig('TestIamPermissions')
      return self._RunMethod(
          config, request, global_params=global_params)

    TestIamPermissions.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}/tasks/{tasksId}:testIamPermissions',
        http_method='POST',
        method_id='batch.projects.locations.tasks.testIamPermissions',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=[],
        relative_path='v1alpha1/{+resource}:testIamPermissions',
        request_field='testIamPermissionsRequest',
        request_type_name='BatchProjectsLocationsTasksTestIamPermissionsRequest',
        response_type_name='TestIamPermissionsResponse',
        supports_download=False,
    )

  class ProjectsLocationsService(base_api.BaseApiService):
    """Service class for the projects_locations resource."""

    _NAME = 'projects_locations'

    def __init__(self, client):
      super(BatchV1alpha1.ProjectsLocationsService, self).__init__(client)
      self._upload_configs = {
          }

    def Get(self, request, global_params=None):
      r"""Gets information about a location.

      Args:
        request: (BatchProjectsLocationsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Location) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations/{locationsId}',
        http_method='GET',
        method_id='batch.projects.locations.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1alpha1/{+name}',
        request_field='',
        request_type_name='BatchProjectsLocationsGetRequest',
        response_type_name='Location',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists information about the supported locations for this service.

      Args:
        request: (BatchProjectsLocationsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListLocationsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1alpha1/projects/{projectsId}/locations',
        http_method='GET',
        method_id='batch.projects.locations.list',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['filter', 'pageSize', 'pageToken'],
        relative_path='v1alpha1/{+name}/locations',
        request_field='',
        request_type_name='BatchProjectsLocationsListRequest',
        response_type_name='ListLocationsResponse',
        supports_download=False,
    )

  class ProjectsService(base_api.BaseApiService):
    """Service class for the projects resource."""

    _NAME = 'projects'

    def __init__(self, client):
      super(BatchV1alpha1.ProjectsService, self).__init__(client)
      self._upload_configs = {
          }
