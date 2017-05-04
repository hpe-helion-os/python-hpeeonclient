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


from eonclient.common import http
from eonclient.v2 import api

PWD_SIZE = 20


class Client(object):
    """Client for the Eon v2 API.

    :param string endpoint: A user-supplied endpoint URL for the eon
                            service.
    :param function token: Provides token for authentication.
    :param integer timeout: Allows customization of the timeout for client
                            http requests. (optional)
    """

    def __init__(self, *args, **kwargs):
        """Initialize a new client for the Eon v1 API."""
        self.http_client = http.HTTPClient(*args, **kwargs)
        self.api = api.API(self.http_client)

    def get_resource_mgr_list(self, _type=None):
        response, body = self.api.get_resource_mgr_list(_type)
        return body

    def get_resource_mgr(self, _id):
        response, body = self.api.get_resource_mgr(_id)
        return body

    def add_resource_mgr(self, data):
        response, body = self.api.add_resource_mgr(data)
        return body

    def update_resource_mgr(self, _id, data):
        response, body = self.api.update_resource_mgr(_id, data)
        return body

    def delete_resource_mgr(self, _id):
        response, body = self.api.delete_resource_mgr(_id)
        return response, body

    def get_resource_list(self, _type=None, state=None,
                          list_supported_types=None):
        response, body = self.api.get_resource_list(_type, state,
                                                    list_supported_types)
        return body

    def get_resource(self, _id):
        response, body = self.api.get_resource(_id)
        return body

    def add_resource(self, data):
        response, body = self.api.add_resource(data)
        return body

    def update_resource(self, _id, data):
        response, body = self.api.update_resource(_id, data)
        return response, body

    def delete_resource(self, _id):
        response, body = self.api.delete_resource(_id)
        return response, body

    def activate_resource(self, _id, data):
        response, body = self.api.activate_resource(_id, data)
        return body

    def provision_resource(self, _id, data):
        response, body = self.api.provision_resource(_id, data)
        return body

    def deactivate_resource(self, _id, data):
        response, body = self.api.deactivate_resource(_id, data)
        return body

    def get_resource_template(self, type_, data=None):
        _, body = self.api.get_resource_template(type_, data)
        return body
