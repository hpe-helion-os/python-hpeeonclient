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

HTTP_ARGS = ('http://localhost:8282/',)
HTTP_KWARGS = {'insecure': False,
               'token': 'TOKEN',
               'timeout': 600,
               'cacert': None,
               'key_file': '',
               'cert_file': '',
               'fixture': {'url': None,
                           'method': None,
                           'retval': None}}

rsc_mgr_id = '305ff8ea-15ee-4401-ab1e-ff12623986de'
rsc_id = 'e83eae4c-ce79-45f4-9d72-0af9541801d2'

vc_data = {
    'name': 'test_vc',
    'ip_address': '10.1.1.10',
    'username': 'admin',
    'password': 'password',
    'port': '443',
    'type': 'vcenter'}

vc_data1 = {
    'name': 'test_vc1',
    'ip_address': '10.1.1.40',
    'username': 'admin',
    'password': 'password',
    'port': '443',
    'type': 'vcenter'}

rhel_data = {
    'name': 'RHNode1',
    'type': 'rhel',
    'state': 'imported',
    'ip_address': '10.1.1.50',
    'username': 'rhel_admin',
    'password': 'rhel_password'}

rhel_data1 = {
    'name': 'rhelnode_1',
    'type': 'rhel',
    'state': 'imported',
    'ip_address': '10.1.1.60',
    'username': 'admin_rhel',
    'password': 'password_rhel'}

post_vc_data = {
    "username": "administrator@vsphere.local",
    "name": "vcenter-01",
    "ip_address": "10.1.200.38",
    "password": "init123#",
    "type": "vcenter",
    "port": "443"}

post_fixture = {
    'url': 'v2/resource_mgrs',
    'method': 'POST',
    'retval': {"username": "administrator@vsphere.local",
               "name": "vcenter-01",
               "ip_address": "10.1.200.38",
               "id": "585fd1ff-167e-4c99-bb04-e7da7fef5ce6",
               "meta_data": [],
               "password": "init123#",
               "type": "vcenter",
               "port": "443"}
}

put_fixture = {
    'url': 'v2/resource_mgrs',
    'method': 'PUT',
    'retval': {"username": "user@vsphere.local",
               "name": "vcenter-updated",
               "ip_address": "10.1.200.38",
               "id": "585fd1ff-167e-4c99-bb04-e7da7fef5ce6",
               "meta_data": [],
               "password": "init123#",
               "type": "vcenter",
               "port": "443"}
}

get_all_fixture = {
    'url': 'v2/resource_mgrs',
    'method': 'GET',
    'retval': [
        {"username": "administrator@vsphere.local",
         "name": "vcenter-01",
         "ip_address": "10.1.200.38",
         "id": "585fd1ff-167e-4c99-bb04-e7da7fef5ce6",
         "meta_data": [],
         "password": "init123#",
         "type": "vcenter",
         "port": "443"},

        {"username": "helion",
         "name": "vcenter-02",
         "ip_address": "10.1.200.17",
         "id": "968f0b45-83b4-4292-8376-0585ca9aa80b",
         "meta_data": [],
         "password": "gone2far",
         "type": "vcenter",
         "port": "443"}
    ]
}

get_fixture = {
    'url': 'v2/resource_mgrs/585fd1ff-167e-4c99-bb04-e7da7fef5ce6',
    'method': 'GET',
    'retval': {
        "username": "administrator@vsphere.local",
        "name": "vcenter-01",
        "ip_address": "10.1.200.38",
        "id": "585fd1ff-167e-4c99-bb04-e7da7fef5ce6",
        "meta_data": [],
        "inventory":
            {"info": {
                "vcenter_uuid": "BC9DED4E-1639-481D-B190-2B54A2BF5674"},
             "resources":
                 {"datacenter": {
                     "count": 2,
                     "datacenter-2":
                         {"clusters": {"domain-c21": "Cluster1"},
                          "name": "DC1",
                          "clusters_count": 1},
                     "datacenter-179":
                         {"clusters": {"domain-c184": "Cluster2"},
                          "name": "DC2",
                          "clusters_count": 1}}}},
        "password": "init123#",
        "type": "vcenter",
        "port": "443"}
}
get_fixture_id = "585fd1ff-167e-4c99-bb04-e7da7fef5ce6"
get_fixture_uuid = "BC9DED4E-1639-481D-B190-2B54A2BF5674"

delete_fixture = {
    'url':
        'v2/resource_mgrs/585fd1ff-167e-4c99-bb04-e7da7fef5ce6',
    'method': 'DELETE',
    'retval': None}

get_all_fixture_resource = {
    'url': 'v2/resources',
    'method': 'GET',
    'retval': [
        {"username": "UNSET",
         "name": "HOS-Cluster",
         "ip_address": "UNSET",
         "state": "imported",
         "id": "2160ce3c-1f54-457f-82d0-1acb9fbb32c7",
         "resource_mgr_id":
             "6542e282-00ac-47a5-9c84-d107604bfb09",
         "meta_data":
             [{"name": "cluster_moid",
               "value": "domain-c21",
               "id": "52ac02d1-3a44-48f5-8384-f5df145806ed"}],
         "password": "UNSET", "type": "esxcluster",
         "port": "UNSET"},
        {"username": "UNSET", "name": "Cluster1",
         "ip_address": "UNSET", "state": "imported",
         "id": "a758b20c-3f42-4173-9d7e-8ab48da4538c",
         "resource_mgr_id":
             "8d3a4454-63c2-40ae-9c98-34dfd9ad9add",
         "meta_data":
             [{"name": "cluster_moid",
               "value": "domain-c21",
               "id": "a732b85f-bd11-4859-9067-f615eba03934"}],
         "password": "UNSET", "type": "esxcluster",
         "port": "UNSET"},
        {"username": "UNSET", "name": "Cluster2",
         "ip_address": "UNSET", "state": "imported",
         "id": "e12cc99d-4dff-432e-bc61-b9553b0dd0ef",
         "resource_mgr_id":
             "8d3a4454-63c2-40ae-9c98-34dfd9ad9add",
         "meta_data":
             [{"name": "cluster_moid",
               "value": "domain-c184",
               "id": "e83eae4c-ce79-45f4-9d72-0af9541801d2"}],
         "password": "UNSET", "type": "esxcluster",
         "port": "UNSET"}]
}

get_fixture_resource_id = "a758b20c-3f42-4173-9d7e-8ab48da4538c"
get_fixture_resource_mgr_id = "8d3a4454-63c2-40ae-9c98-34dfd9ad9add"
get_fixture_resource = {
    'url': 'v2/resources/a758b20c-3f42-4173-9d7e-8ab48da4538c',
    'method': 'GET',
    'retval': {
        "username": "UNSET",
        "name": "Cluster1",
        "ip_address": "UNSET",
        "state": "imported",
        "id": "a758b20c-3f42-4173-9d7e-8ab48da4538c",
        "resource_mgr_id": "8d3a4454-63c2-40ae-9c98-34dfd9ad9add",
        "meta_data": [{"name": "cluster_moid", "value": "domain-c21",
                       "id": "a732b85f-bd11-4859-9067-f615eba03934"}],
        "inventory": {"datacenter": {"moid": "datacenter-2", "name": "DC1"},
                      "hosts": [
                          {"connection_state": "connected", "moid": "host-542",
                           "name": "10.1.200.130", "vms": 7},
                          {"connection_state": "connected", "moid": "host-25",
                           "name": "10.1.200.157", "vms": 1}]},
        "resource_manager_info": {"username": "administrator@vsphere.local",
                                  "name": "vc1", "ip_address": "10.1.200.38",
                                  "id": "8d3a4454-63c2-40ae-9c98-34dfd9ad9add",
                                  "meta_data": [], "password": "init123#",
                                  "type": "vcenter", "port": "443"},
        "password": "UNSET",
        "type": "esxcluster",
        "port": "UNSET"}
}

esxcluster_inv_keys = ['datacenter', 'hosts']

delete_fixture_resource = {
    'url': 'v2/resources/a758b20c-3f42-4173-9d7e-8ab48da4538c',
    'method': 'DELETE',
    'retval': None}

net_conf_dict = {"network_properties": {
    "hlm_version": "2.1",
    "network": {
        "deployer_network": {
            "deployer_pg_name": "ESX-CONF-PG",
            "deployer_vlan": "100",
            "vlan_type": "trunk",
            "enable_deployer_dhcp": "false",
            "deployer_cidr": "10.20.18.0/23",
            "ip_range": {
                "start_address": "",
                "end_address": ""
            },
            "deployer_gateway_ip": "10.20.18.1",
            "deployer_node_ip": "10.20.16.2"
        },
        "management_network": {
            "mgmt_dvs_name": "MGMT-DVS",
            "mgmt_nic_name": "vmnic3",
            "mgmt_pg_name": "MGMT-PG",
            "mgmt_vlan": "0,1-4094",
            "vlan_type": "trunk",
            "mgmt_interface_order": "eth1",
            "active_nics": "",
            "load_balancing": "1",
            "network_failover_detection": "1",
            "notify_switches": "yes"
        },

        "trunk_network": {
            "trunk_dvs_name": "TRUNK-DVS",
            "trunk_pg_name": "TRUNK-PG",
            "trunk_interface_order": "eth2"
        },
        "tenant_network_type": "vlan",
        "vlan_range": "1-4094"
    },

    "template": {
        "template_name": "hlm-template"
    },

    "vmconfig": {
        "cpu": "4",
        "memory_in_mb": "4096",
        "ssh_key": "SSH_CERTIFICATE_CONTENTS"
    }
}}

activate_fixture_resource = {
    'url': 'v2/resources/a758b20c-3f42-4173-9d7e-8ab48da4538c/activate/',
    'method': 'POST',
    'retval': net_conf_dict
}

deactivate_fixture_resource = {
    'url': 'v2/resources/a758b20c-3f42-4173-9d7e-8ab48da4538c/deactivate/',
    'method': 'DELETE',
    'retval': dict()
}

deactivate_forced_dict = {'forced': True}
