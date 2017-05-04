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


import copy
import hashlib
import fixtures
import six
import testtools

from eonclient.common import http


class BaseTestCase(testtools.TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.useFixture(fixtures.FakeLogger())


class FakeAPI(object):
    def __init__(self, fixtures):
        self.fixtures = fixtures
        self.calls = []

    def _request(self, method, url, headers=None, body=None):
        call = (method, url, headers or {}, body)
        self.calls.append(call)
        return self.fixtures[url][method]

    def raw_request(self, *args, **kwargs):
        fixture = self._request(*args, **kwargs)
        body_iter = http.ResponseBodyIterator(six.StringIO(fixture[1]))
        return FakeResponse(fixture[0]), body_iter

    def json_request(self, *args, **kwargs):
        fixture = self._request(*args, **kwargs)
        return FakeResponse(fixture[0]), fixture[1]


class FakeResponse(object):
    def __init__(self, headers, body=None, version=None):
        """:param headers: dict representing HTTP response headers
        :param body: file-like object
        """
        self.headers = headers
        self.body = body

    def getheaders(self):
        return copy.deepcopy(self.headers).items()

    def getheader(self, key, default):
        return self.headers.get(key, default)

    def read(self, amt):
        return self.body.read(amt)

VC_ID = "300c7d61-fea0-4662-9907-451247321040"
VC_IP = "1.1.2.2"
VC_NAME = "testvc1"
VC_PASS = "test123"
VC_USER = "user1@vsphere.local"

VC_IP_1 = "3.3.2.2"
VC_USER_1 = "user2@vsphere.local"

CLUSTER_MOID = "domain-c1123"
CLUSTER_NAME = "Cluster1"
PXY_SERVER_ID = hashlib.sha1(VC_ID+CLUSTER_MOID).hexdigest()
PXY_SERVER_IP = "3.3.3.3"

VC_DATA = {
              "vcenter_meta": {
                "username": VC_USER,
                "password": VC_PASS,
                "name": VC_NAME,
                "ip_address": VC_IP,
                "id": VC_ID,
                "port": 443,
              }
}
VC_INFO = {
                "username": VC_USER,
                "name": VC_NAME,
                "ip_address": VC_IP,
                "id": VC_ID,
                "port": 443,
              }

VC_INFO_1 = {
                "username": VC_USER_1,
                "name": VC_NAME,
                "ip_address": VC_IP_1,
                "id": VC_ID,
                "port": 443,
              }


PROXY_NODE = [{
    "pxe-mac-addr": "00:50:56:ae:59:7a",
    "pxe-ip-addr": PXY_SERVER_IP,
    "name": PXY_SERVER_ID,
    "cluster-moid": CLUSTER_MOID,
    "cluster": CLUSTER_NAME,
  }]

PROXY_SERVER = {
    "id": PXY_SERVER_ID,
    "ip-addr": PXY_SERVER_IP,
    "role": "ESX-COMPUTE-ROLE"
    }

PASS_THRU = {'product': {'version': 2}, 'pass-through': {'servers': []}}

PROXY_PASS_THRU = {
    'product': {'version': 2},
    'pass-through':

        {'servers': [{
            "data": {
                "vmware": {
                    "cert_check": False,
                    "vcenter_cluster": CLUSTER_NAME,
                    "vcenter_id": VC_ID,
                    "vcenter_ip": VC_IP,
                    "vcenter_username": VC_USER,
                    "vcenter_port": 443
                }
            },
            "id": PXY_SERVER_ID
        }
        ]
        }}

PROXY_PASS_THRU_SERVER = {
        "data": {
          "vmware": {
            "cert_check": False,
            "vcenter_cluster": CLUSTER_NAME,
            "vcenter_id": VC_ID,
            "vcenter_ip": VC_IP,
            "vcenter_username": VC_USER,
            "vcenter_port": 443
          }
        },
        "id": PXY_SERVER_ID
      }

PROXY_PASS_THRU_1 = copy.deepcopy(PROXY_PASS_THRU)
PROXY_PASS_THRU_1['pass-through']['servers'][0]['data']['vmware'][
    'vcenter_username'] = VC_USER_1
PROXY_PASS_THRU_1['pass-through']['servers'][0]['data']['vmware'][
    'vcenter_ip'] = VC_IP_1

PROXY_PASS_THRU_SERVER_1 = {
        "data": {
          "vmware": {
            "cert_check": False,
            "vcenter_cluster": CLUSTER_NAME,
            "vcenter_id": VC_ID,
            "vcenter_ip": VC_IP_1,
            "vcenter_username": VC_USER_1,
            "vcenter_port": 443
          }
        },
        "id": PXY_SERVER_ID
      }

HOST_MOID_1 = "domain-h111"
HOST_MOID_2 = "domaon-h222"
HOST_NAME_1 = "esx1.test.com"
HOST_NAME_2 = "esx2.test.com"
NW_SERVER_ID_1 = hashlib.sha1(VC_ID+HOST_MOID_1).hexdigest()
NW_SERVER_ID_2 = hashlib.sha1(VC_ID+HOST_MOID_2).hexdigest()
NW_SERVER_IP_1 = "1.1.1.1"
NW_SERVER_IP_2 = "2.2.2.2"
CLUSTER_DVS_MAPPINGS = "Datacenter/host/"+CLUSTER_NAME+":OVSvApp-Trunk"

NW_NODE = [
      {
        "pxe-mac-addr": "00:50:56:ex:46:d1",
        "esx_hostname": HOST_NAME_1,
        "host-moid": HOST_MOID_1,
        "ovsvapp_node": "ovsvapp-15-212-181-202",
        "pxe-ip-addr": NW_SERVER_IP_1,
        "cluster_dvs_mapping": CLUSTER_DVS_MAPPINGS,
        "cluster": CLUSTER_NAME,
        "name": NW_SERVER_ID_1
      },
      {
        "pxe-mac-addr": "00:50:56:ex:46:d5",
        "esx_hostname": HOST_NAME_2,
        "host-moid": HOST_MOID_2,
        "ovsvapp_node": "ovsvapp-15-212-181-201",
        "pxe-ip-addr": NW_SERVER_IP_2,
        "cluster_dvs_mapping": CLUSTER_DVS_MAPPINGS,
        "cluster": CLUSTER_NAME,
        "name": NW_SERVER_ID_2
      }
    ]

NW_SERVER_1 = {
    "id": NW_SERVER_ID_1,
    "ip-addr": NW_SERVER_IP_1,
    "role": "OVSVAPP-ROLE"
    }

NW_SERVER_2 = {
    "id": NW_SERVER_ID_2,
    "ip-addr": NW_SERVER_IP_2,
    "role": "OVSVAPP-ROLE"
    }

NW_PASS_THRU = {
    'product': {'version': 2},
    'pass-through':
        {'servers': [{
            "data": {
                "vmware": {
                    "cert_check": False,
                    "vcenter_cluster": CLUSTER_NAME,
                    "vcenter_id": VC_ID,
                    "vcenter_ip": VC_IP,
                    "vcenter_username": VC_USER,
                    "vcenter_port": 443,
                    "esx_hostname": HOST_NAME_1,
                    "cluster_dvs_mapping": CLUSTER_DVS_MAPPINGS
                }
            },
            "id": NW_SERVER_ID_1
        },
            {
                "data": {
                    "vmware": {
                        "cert_check": False,
                        "vcenter_cluster": CLUSTER_NAME,
                        "vcenter_id": VC_ID,
                        "vcenter_ip": VC_IP,
                        "vcenter_username": VC_USER,
                        "vcenter_port": 443,
                        "esx_hostname": HOST_NAME_2,
                        "cluster_dvs_mapping": CLUSTER_DVS_MAPPINGS
                    }
                },
                "id": NW_SERVER_ID_2
            }
        ]
        }}

NW_PASS_THRU_1 = {
    'product': {'version': 2},
    'pass-through':
        {'servers': [{
            "data": {
                "vmware": {
                    "cert_check": False,
                    "vcenter_cluster": CLUSTER_NAME,
                    "vcenter_id": VC_ID,
                    "vcenter_ip": VC_IP_1,
                    "vcenter_username": VC_USER_1,
                    "vcenter_port": 443,
                    "esx_hostname": HOST_NAME_1,
                    "cluster_dvs_mapping": CLUSTER_DVS_MAPPINGS
                }
            },
            "id": NW_SERVER_ID_1
        },
            {
                "data": {
                    "vmware": {
                        "cert_check": False,
                        "vcenter_cluster": CLUSTER_NAME,
                        "vcenter_id": VC_ID,
                        "vcenter_ip": VC_IP_1,
                        "vcenter_username": VC_USER_1,
                        "vcenter_port": 443,
                        "esx_hostname": HOST_NAME_2,
                        "cluster_dvs_mapping": CLUSTER_DVS_MAPPINGS
                    }
                },
                "id": NW_SERVER_ID_2
            }
        ]
        }}

PROXY_NW_PASS_THRU = copy.deepcopy(NW_PASS_THRU)
PROXY_NW_PASS_THRU_11 = copy.deepcopy(NW_PASS_THRU)
PROXY_NW_PASS_THRU_1 = copy.deepcopy(NW_PASS_THRU_1)

PROXY_NW_PASS_THRU['pass-through']['servers'].append(PROXY_PASS_THRU_SERVER)
PROXY_NW_PASS_THRU_11['pass-through']['servers'].append(
    PROXY_PASS_THRU_SERVER_1)
PROXY_NW_PASS_THRU_1['pass-through']['servers'].append(
    PROXY_PASS_THRU_SERVER_1)
