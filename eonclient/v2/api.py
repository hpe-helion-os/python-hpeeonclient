#
# (c) Copyright 2015-2017 Hewlett Packard Enterprise Development Company LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#


"""
This module provides the python client interface for the eon service.
"""
import logging


LOG = logging.getLogger(__name__)


class API(object):
    """
    It provides the required python API for eon REST API.

    To use this API, create the HttpClient with required configuration
    parameters and instantiate as follows.
        http_client = HttpClient(...)
        api = API(http_client)
    """

    def __init__(self, http_client):
        self.http_client = http_client

    def get_resource_mgr_list(self, _type):
        """Retrieve the list of registered Resource Managers

        @:param _type: Type of the Resource Manager. vcenter (or) scvmm
        """
        url_base = "v2/resource_mgrs"
        url = url_base + "?type=%s" % _type if _type else url_base
        response, body = self.http_client.json_request(url=url, method="GET")
        return response, body

    def get_resource_mgr(self, _id):
        """Retrieve the details of the given Resource Manager

        @:param _id: ID of the Resource Manager
        """
        response, body = self.http_client.json_request(
            url="v2/resource_mgrs/%s" % _id,
            method="GET")
        return response, body

    def add_resource_mgr(self, data):
        """Add the Resource Manager

        @:param data: Resource Manager details
         Ex: {
            'name': 'vcenter-01',
            'ip_address': '10.1.1.10',
            'username': 'admin',
            'password': 'password',
            'port': '443',
            'type': 'vcenter'
            }
        """
        response, body = self.http_client.json_request(
            url="v2/resource_mgrs/",
            method="POST",
            body=data)
        return response, body

    def update_resource_mgr(self, _id, data):
        """Update the Resource Manager

        @:param _id: ID of the Resource Manager
        @:param data: Resource Manager details
         Ex: {
            'name': 'vcenter-02',
            'ip_address': '10.1.1.20',
            'username': 'admin',
            'password': 'password',
            'port': '9443'
            }
        """
        response, body = self.http_client.json_request(
            url="v2/resource_mgrs/%s" % _id,
            method="PUT",
            body=data)
        return response, body

    def delete_resource_mgr(self, _id):
        """Delete the Resource Manager

        @:param _id: ID of the Resource Manager
        """
        response, body = self.http_client.json_request(
            url="v2/resource_mgrs/%s" % _id,
            method="DELETE")
        return response, body

    def get_resource_list(self, _type, state, list_supported_types=None):
        """Retrieve the list of registered Resources

        :param _type: Type of the Resource. esxcluster (or) rhel (or) hlinux
        (or) hyperv
        :param state: State of the Resource. imported (or) provisioned (or)
        activated
        """
        url_base = "v2/resources"
        if _type and state:
            url = url_base + "?type=%s&state=%s" % (_type, state)
        elif _type and not state:
            url = url_base + "?type=%s" % _type
        elif state and not _type:
            url = url_base + "?state=%s" % state
        elif list_supported_types:
            url = url_base + "?list_supported_types"
        else:
            url = url_base

        response, body = self.http_client.json_request(url=url, method="GET")
        return response, body

    def get_resource(self, _id):
        """Retrieve the details of the given Resource

        :param _id: ID of the Resource
        """
        response, body = self.http_client.json_request(
            url="v2/resources/%s" % _id,
            method="GET")
        return response, body

    def add_resource(self, data):
        """Add the Resource

        @:param data: Resource details
         Ex: {
            'name': 'rhel-01',
            'ip_address': '10.1.1.40',
            'username': 'admin',
            'password': 'password',
            'port': '443',
            'type': 'rhel'
            }
        """
        response, body = self.http_client.json_request(
            url="v2/resources/",
            method="POST",
            body=data)
        return response, body

    def update_resource(self, _id, data):
        """Update the Resource

        @:param _id: ID of the Resource
        @:param data: Resource details
         Ex: {
            'name': 'rhel-02',
            'ip_address': '10.1.1.30',
            'username': 'admin',
            'password': 'password',
            'port': '9443'
            }
        """
        response, body = self.http_client.json_request(
            url="v2/resources/%s" % _id,
            method="PUT",
            body=data)
        return response, body

    def delete_resource(self, _id):
        """Delete the Resource

        @:param _id: ID of the Resource
        """
        response, body = self.http_client.json_request(
            url="v2/resources/%s" % _id,
            method="DELETE")

        return response, body

    def get_resource_template(self, type_, data):
        response, body = self.http_client.json_request(
            url="v2/resources/%s/get_template/" % type_,
            method="POST", body=data)

        return response, body

    def activate_resource(self, _id, data):
        """Activate the Resource

        @:param _id: ID of the Resource
        @:param data: netconfig json contents
        """
        url = "v2/resources/%s/activate/" % _id
        response, body = self.http_client.json_request(
            url=url, method="POST", body=data)
        return response, body

    def provision_resource(self, _id, data):
        """Activate the Resource

        @:param _id: ID of the Resource
        @:param data: netconfig json contents
        """
        url = "v2/resources/%s/provision/" % _id
        response, body = self.http_client.json_request(
            url=url, method="POST", body=data)
        return response, body

    def deactivate_resource(self, _id, data):
        """Deactivate the Resource

        @:param _id: ID of the Resource
        @:param data: {'forced': True} (or) {'forced': False}
        """
        url = "v2/resources/%s/deactivate/" % _id
        response, body = self.http_client.json_request(
            url=url, method="DELETE", body=data)
        return response, body
