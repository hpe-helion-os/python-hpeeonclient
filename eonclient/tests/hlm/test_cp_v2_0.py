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

import os

from eonclient.tests import utils
from eonclient.v1.hlm.configprocessor import CP
from eonclient.v1.hlm import cp_v2_0
from eonclient.v1.hlm.cp_v2_0 import CP_2_0
from eonclient.v1.hlm import constants

WORK_DIR = '/tmp/'
PASS_THRU_FILE = WORK_DIR + 'pass_through.yml'
SERVER_FILE = WORK_DIR + 'servers.yml'


class CpVersionTwoTest(utils.BaseTestCase):
    def setUp(self):
        super(CpVersionTwoTest, self).setUp()
        cp_v2_0.yml_path = WORK_DIR
        self.cp = CP_2_0('add')

    def _create_server_yml(self):
        filename = WORK_DIR + cp_v2_0.yml_file_list[0]
        data = {}
        server1 = {'id': 'c-1', 'ip-addr': '192.168.10.1', 'role': 'ROLE-CCP'}
        server2 = {'id': 'c-2', 'ip-addr': '192.168.10.2', 'role': 'ROLE-CCP'}
        server3 = {'id': 'c-3', 'ip-addr': '192.168.10.3', 'role': 'ROLE-CCP'}
        data.update({'servers': [server1, server2, server3]})
        data.update({'product': {'version': 2}})
        self.cp.write_file(filename, data)

    def test_create_empty_pass_through_file(self):
        self.assertFalse(os.path.exists(WORK_DIR+cp_v2_0.yml_file_list[1]),
                         msg=cp_v2_0.yml_file_list[1]+' exists')
        self.cp.create_empty_pass_through_file()
        self.assertTrue(os.path.exists(WORK_DIR+cp_v2_0.yml_file_list[1]),
                        msg=cp_v2_0.yml_file_list[1]+' not exists')

    def test_add_server_proxy(self):
        self._create_server_yml()
        cp2 = CP_2_0('add', utils.VC_INFO, utils.PROXY_NODE,
                     constants.COMPUTE_PROXY_ROLE)
        servers = cp2.load_file(SERVER_FILE)['servers']
        self.assertNotIn(utils.PROXY_SERVER, servers)
        cp2.add_server()
        servers = cp2.load_file(SERVER_FILE)['servers']
        self.assertIn(utils.PROXY_SERVER, servers)

    def test_add_server_network_driver_without_proxy(self):
        self._create_server_yml()
        cp2 = CP_2_0('add', utils.VC_INFO, utils.NW_NODE,
                     constants.NETWORK_DRIVER_ROLE)
        servers = cp2.load_file(SERVER_FILE)['servers']
        self.assertNotIn(utils.NW_SERVER_1, servers)
        cp2.add_server()
        servers = cp2.load_file(SERVER_FILE)['servers']
        self.assertIn(utils.NW_SERVER_1, servers)
        self.assertIn(utils.NW_SERVER_2, servers)

    def test_add_server_network_driver_with_proxy(self):
        self._create_server_yml()
        cp2 = CP_2_0('add', utils.VC_INFO)
        servers = cp2.load_file(SERVER_FILE)['servers']
        self.assertNotIn(utils.PROXY_SERVER, servers)

        cp2._node_info = utils.PROXY_NODE
        cp2._role = constants.COMPUTE_PROXY_ROLE
        cp2.add_server()

        cp2._node_info = utils.NW_NODE
        cp2._role = constants.NETWORK_DRIVER_ROLE
        cp2.add_server()

        servers = cp2.load_file(SERVER_FILE)['servers']
        self.assertIn(utils.PROXY_SERVER, servers)
        self.assertIn(utils.NW_SERVER_1, servers)
        self.assertIn(utils.NW_SERVER_2, servers)

    def test_add_pass_through_proxy(self):
        cp2 = CP_2_0('add', utils.VC_INFO, utils.PROXY_NODE,
                     constants.COMPUTE_PROXY_ROLE)
        self.cp.create_empty_pass_through_file()
        servers = cp2.load_file(PASS_THRU_FILE)['pass-through'].get('servers')
        self.assertNotIn(utils.PROXY_SERVER, servers)
        cp2.add_pass_through()
        self.assertEqual(utils.PROXY_PASS_THRU, cp2.load_file(PASS_THRU_FILE))

    def test_add_pass_through_network_driver_without_proxy(self):
        cp2 = CP_2_0('add', utils.VC_INFO, utils.NW_NODE,
                     constants.NETWORK_DRIVER_ROLE)
        self.cp.create_empty_pass_through_file()
        servers = cp2.load_file(PASS_THRU_FILE)['pass-through'].get('servers')
        self.assertNotIn(utils.NW_SERVER_1, servers)
        cp2.add_pass_through()
        self.assertEqual(utils.NW_PASS_THRU, cp2.load_file(PASS_THRU_FILE))

    def test_add_pass_through_network_driver_with_proxy(self):
        self.cp.create_empty_pass_through_file()
        self.assertIsNone(CP.load_file(PASS_THRU_FILE)[
                              'pass-through'].get('servers'))

        cp2 = CP_2_0('add', utils.VC_INFO)

        cp2._node_info = utils.PROXY_NODE
        cp2._role = constants.COMPUTE_PROXY_ROLE
        cp2.add_pass_through()
        self.assertEqual(utils.PROXY_PASS_THRU, cp2.load_file(PASS_THRU_FILE))

        cp2._node_info = utils.NW_NODE
        cp2._role = constants.NETWORK_DRIVER_ROLE
        cp2.add_pass_through()
        self.assertItemsEqual(utils.PROXY_NW_PASS_THRU,
                              cp2.load_file(PASS_THRU_FILE))

    def test_update_pass_through_network_driver_with_proxy(self):
        self.cp.create_empty_pass_through_file()
        self.assertIsNone(CP.load_file(PASS_THRU_FILE)[
                              'pass-through'].get('servers'))

        cp2 = CP_2_0('add', utils.VC_INFO)

        cp2._node_info = utils.PROXY_NODE
        cp2._role = constants.COMPUTE_PROXY_ROLE
        cp2.add_pass_through()
        cp2._node_info = utils.NW_NODE
        cp2._role = constants.NETWORK_DRIVER_ROLE
        cp2.add_pass_through()

        cp2 = CP_2_0('add', utils.VC_INFO_1)

        cp2._node_info = utils.PROXY_NODE
        cp2._role = constants.COMPUTE_PROXY_ROLE
        cp2.add_pass_through()
        self.assertItemsEqual(utils.PROXY_NW_PASS_THRU_11,
                              cp2.load_file(PASS_THRU_FILE))

        cp2._node_info = utils.NW_NODE
        cp2._role = constants.NETWORK_DRIVER_ROLE
        cp2.add_pass_through()
        self.assertItemsEqual(utils.PROXY_NW_PASS_THRU_1,
                              cp2.load_file(PASS_THRU_FILE))

    def test_delete_server_proxy(self):
        self._create_server_yml()
        cp2 = CP_2_0('add', utils.VC_INFO, utils.PROXY_NODE,
                     constants.COMPUTE_PROXY_ROLE)
        cp2.add_server()
        servers = cp2.load_file(SERVER_FILE)['servers']
        self.assertIn(utils.PROXY_SERVER, servers)

        cp2._action = 'delete'
        cp2.delete_server()
        servers = cp2.load_file(SERVER_FILE)['servers']
        self.assertNotIn(utils.PROXY_SERVER, servers)

    def test_delete_server_network_driver(self):
        self._create_server_yml()
        cp2 = CP_2_0('add', utils.VC_INFO, utils.NW_NODE,
                     constants.NETWORK_DRIVER_ROLE)
        cp2.add_server()
        servers = cp2.load_file(SERVER_FILE)['servers']
        self.assertIn(utils.NW_SERVER_1, servers)
        self.assertIn(utils.NW_SERVER_2, servers)

        cp2._action = 'delete'
        cp2.delete_server()
        servers = cp2.load_file(SERVER_FILE)['servers']
        self.assertNotIn(utils.NW_SERVER_1, servers)
        self.assertNotIn(utils.NW_SERVER_2, servers)

    def test_delete_pass_through_proxy(self):
        cp2 = CP_2_0('add', utils.VC_INFO, utils.PROXY_NODE,
                     constants.COMPUTE_PROXY_ROLE)
        self.cp.create_empty_pass_through_file()

        cp2.add_pass_through()
        self.assertEqual(utils.PROXY_PASS_THRU, cp2.load_file(PASS_THRU_FILE))

        cp2._action = 'delete'
        cp2.delete_pass_through()
        self.assertEqual(utils.PASS_THRU, cp2.load_file(PASS_THRU_FILE))

    def test_delete_pass_through_network_driver_without_proxy(self):
        cp2 = CP_2_0('add', utils.VC_INFO, utils.NW_NODE,
                     constants.NETWORK_DRIVER_ROLE)
        self.cp.create_empty_pass_through_file()

        cp2.add_pass_through()
        self.assertEqual(utils.NW_PASS_THRU, cp2.load_file(PASS_THRU_FILE))

        cp2._action = 'delete'
        cp2.delete_pass_through()
        self.assertEqual(utils.PASS_THRU, cp2.load_file(PASS_THRU_FILE))

    def test_delete_pass_through_network_driver_with_proxy(self):
        cp2 = CP_2_0('add', utils.VC_INFO, utils.PROXY_NODE,
                     constants.COMPUTE_PROXY_ROLE)
        self.cp.create_empty_pass_through_file()
        cp2.add_pass_through()
        self.assertEqual(utils.PROXY_PASS_THRU, cp2.load_file(PASS_THRU_FILE))

        cp2._node_info = utils.NW_NODE
        cp2._role = constants.NETWORK_DRIVER_ROLE

        cp2.add_pass_through()
        self.assertEqual(sorted(utils.PROXY_NW_PASS_THRU),
                         sorted(cp2.load_file(PASS_THRU_FILE)))

        cp2._action = 'delete'
        cp2.delete_pass_through()
        self.assertEqual(utils.PROXY_PASS_THRU, cp2.load_file(PASS_THRU_FILE))

    def tearDown(self):
        super(CpVersionTwoTest, self).tearDown()
        for f in cp_v2_0.yml_file_list:
            file = '/tmp/'+f
            if os.path.exists(file):
                os.remove(file)
                pass
