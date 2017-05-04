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
from eonclient.tests import utils
from eonclient.v2 import client
from eonclient.v2 import api

RESPONSE200 = 200


class FakeClient(client.Client):
    def __init__(self, *args, **kwargs):
        super(FakeClient, self).__init__(*args, **kwargs)
        self.http_client = FakeHTTPClient(*args, **kwargs)
        self.api = FakeAPI(self.http_client)

    def assert_called_with(self, method, url, body=None):

        if method in ['GET', 'DELETE']:
            assert body is None
        elif method in ['PUT', 'POST']:
            assert body is not None

        assert method == self.http_client.method
        assert url == self.http_client.url

    def assert_return(self, expected):
        assert expected == self.http_client.body

    def assert_vcenter_return(self, expected):
        required_field = ['username', 'name', 'ip_address', 'id', 'meta_data',
                          'password', 'type']
        for fl in required_field:
            assert fl in expected

    def assert_resource_return(self, expected):
        required_fields = ['username', 'name', 'ip_address', 'id', 'meta_data',
                           'password', 'type', 'state', 'resource_mgr_id']
        for fl in required_fields:
            assert fl in expected


class FakeHTTPClient(http.HTTPClient):
    def __init__(self, *args, **kwargs):
        super(FakeHTTPClient, self).__init__(*args, **kwargs)
        self.fixture = kwargs.get('fixture')
        self.url = None
        self.method = None
        self.body = None

    def json_request(self, url=None, method=None, **kwargs):
        self.url = url
        self.method = method
        self.body = self.fixture.get('retval')
        resp = utils.FakeResponse({})
        resp.status = RESPONSE200
        return resp, self.body


class FakeAPI(api.API):
    def __init__(self, http_client):
        super(FakeAPI, self).__init__(http_client)
        self.http_client = http_client
