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

from eonclient.tests import utils
from eonclient.tests.v2 import fakes
from eonclient.tests.v2 import test_data


class ResourceManagerTests(utils.BaseTestCase):
    def setUp(self):
        super(ResourceManagerTests, self).setUp()

    def _get_fake_client(self, method):
        kwargs = test_data.HTTP_KWARGS
        if method == 'post':
            kwargs.update({'fixture': test_data.post_fixture})
        elif method == 'get_all':
            kwargs.update({'fixture': test_data.get_all_fixture})
        elif method == 'get':
            kwargs.update({'fixture': test_data.get_fixture})
        elif method == 'delete':
            kwargs.update({'fixture': test_data.delete_fixture})
        elif method == 'put':
            kwargs.update({'fixture': test_data.put_fixture})

        return fakes.FakeClient(*test_data.HTTP_ARGS, **kwargs)

    def test_resource_manager_add(self):
        self.client = self._get_fake_client('post')
        mgr = self.client.add_resource_mgr(test_data.post_vc_data)
        self.assertEqual(mgr, test_data.post_fixture.get('retval'))
        self.client.assert_vcenter_return(mgr)

    def test_resource_manager_update(self):
        self.client = self._get_fake_client('put')
        mgr = self.client.update_resource_mgr(
            test_data.get_fixture_resource_mgr_id,
            test_data.put_fixture.get('retval'))
        self.assertEqual(mgr, test_data.put_fixture.get('retval'))
        self.client.assert_vcenter_return(mgr)

    def test_resource_manager_list(self):
        self.client = self._get_fake_client('get_all')
        mgr_list = self.client.get_resource_mgr_list()
        self.assertEqual(mgr_list, test_data.get_all_fixture.get('retval'))
        self.assertEqual(len(mgr_list), 2)
        [self.client.assert_vcenter_return(mgr) for mgr in mgr_list]

    def test_resource_manager_get(self):
        self.client = self._get_fake_client('get')
        mgr = self.client.get_resource_mgr(test_data.get_fixture_id)
        self.client.assert_vcenter_return(mgr)
        mgr_inv = mgr.get('inventory')
        self.assertEqual(mgr_inv.get('info').get('vcenter_uuid'),
                         test_data.get_fixture_uuid)
        self.assertEqual(
            len(mgr_inv.get('resources').get('datacenter').keys()), 3)

    def test_resource_manager_delete(self):
        self.client = self._get_fake_client('delete')
        self.assertIsNone(self.client.delete_resource_mgr(
            test_data.get_fixture_id))
