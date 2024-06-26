# -*- coding: utf-8 -*- #
# Copyright 2022 Google LLC. All Rights Reserved.
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
"""Base ResourceBuilder for Cloud Run Integrations."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import abc
import re


class TypeKit(object):
  """An abstract class that represents a typekit."""

  def __init__(self, type_metadata):
    self._type_metadata = type_metadata

  @property
  def integration_type(self):
    return self._type_metadata['integration_type']

  @property
  def resource_type(self):
    return self._type_metadata['resource_type']

  @property
  def is_singleton(self):
    return self._type_metadata.get('singleton', False)

  @property
  def singleton_name(self):
    return self._type_metadata.get('singleton_name')

  @abc.abstractmethod
  def GetAllReferences(self, resource_config):
    return []

  @abc.abstractmethod
  def UpdateResourceConfig(self, parameters, resource_config):
    """Updates config according to the parameters.

    Each TypeKit should override this method to update the resource config
    specific to the need of the typekit.

    Args:
      parameters: dict, parameters from the command
      resource_config: dict, the resource config object of the integration
    """

  def BindServiceToIntegration(self, integration_name, resource_config,
                               service_name, service_config, parameters):
    """Binds a service to the integration.

    Args:
      integration_name: str, name of the integration
      resource_config: dict, the resource config object of the integration
      service_name: str, name of the service
      service_config: dict, the resouce config object of the service
      parameters: dict, parameters from the command
    """
    del resource_config, service_name, parameters  # Not used here.
    ref_to_add = '{}/{}'.format(self.resource_type, integration_name)
    # Check if ref already exists.
    refs = set(ref['ref'] for ref in service_config.get('resources', []))
    if ref_to_add not in refs:
      service_config.setdefault('resources', []).append(
          {'ref': ref_to_add})

  def UnbindServiceFromIntegration(self, integration_name, resource_config,
                                   service_name, service_config, parameters):
    """Unbinds a service from the integration.

    Args:
      integration_name: str, name of the integration
      resource_config: dict, the resource config object of the integration
      service_name: str, name of the service
      service_config: dict, the resouce config object of the service
      parameters: dict, parameters from the command
    """
    del resource_config, service_name, parameters  # Not used here.
    ref_to_remove = '{}/{}'.format(self.resource_type, integration_name)
    service_config['resources'] = [
        x for x in service_config.get('resources', [])
        if x['ref'] != ref_to_remove
    ]

  def NewIntegrationName(self, service, parameters, resources_map):
    """Returns a name for a new integration.

    Args:
      service: str, name of the service
      parameters: dict, parameters from the command
      resources_map: the map of all resources in the application

    Returns:
      str, a new name for the integration.
    """
    del parameters  # Not used in here.
    name = '{}-{}'.format(self.integration_type, service)
    while name in resources_map:
      # If name already taken, tries adding an integer suffix to it.
      # If suffixed name also exists, tries increasing the number until finding
      # an available one.
      count = 1
      match = re.search(r'(.+)-(\d+)$', name)
      if match:
        name = match.group(1)
        count = int(match.group(2)) + 1
      name = '{}-{}'.format(name, count)
    return name

  def GetCreateSelectors(self,
                         integration_name,
                         add_service_name,
                         remove_service_name=None):
    """Returns create selectors for given integration and service.

    Args:
      integration_name: str, name of integration.
      add_service_name: str, name of the service being added.
      remove_service_name: str, name of the service being removed.

    Returns:
      list of dict typed names.
    """
    service_name = add_service_name or remove_service_name
    selectors = [{'type': self.resource_type, 'name': integration_name}]

    if service_name:
      selectors.append({'type': 'service', 'name': service_name})

    return selectors

  def GetDeleteSelectors(self, integration_name):
    """Returns selectors for deleting the integration.

    Args:
      integration_name: str, name of integration.

    Returns:
      list of dict typed names.
    """
    return [{'type': self.resource_type, 'name': integration_name}]
