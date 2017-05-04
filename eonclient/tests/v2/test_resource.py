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


class ResourceTests(utils.BaseTestCase):
    def setUp(self):
        super(ResourceTests, self).setUp()

    def _get_fake_client(self, method):
        kwargs = test_data.HTTP_KWARGS
        if method == 'get_all':
            kwargs.update({'fixture': test_data.get_all_fixture_resource})
        elif method == 'get':
            kwargs.update({'fixture': test_data.get_fixture_resource})
        elif method == 'delete':
            kwargs.update({'fixture': test_data.delete_fixture_resource})
        elif method == 'activate':
            kwargs.update({'fixture': test_data.activate_fixture_resource})
        elif method == 'deactivate':
            kwargs.update({'fixture': test_data.deactivate_fixture_resource})

        return fakes.FakeClient(*test_data.HTTP_ARGS, **kwargs)

    def to_test_resource_add(self):
        # TODO: After integrating with kvm/hyperv/rhel.
        # EsxCluster resource doesn't need resource_add
        pass

    def to_test_resource_update(self):
        # TODO: After host commissioning is implemented (only for esxcluster)
        pass

    def test_resource_list(self):
        self.client = self._get_fake_client('get_all')
        rsc_list = self.client.get_resource_list()
        self.assertEqual(rsc_list,
                         test_data.get_all_fixture_resource.get('retval'))
        self.assertEqual(len(rsc_list), 3)
        [self.client.assert_resource_return(mgr) for mgr in rsc_list]

    def test_resource_get_cluster(self):
        self.client = self._get_fake_client('get')
        rsc = self.client.get_resource(test_data.get_fixture_resource_id)
        self.client.assert_resource_return(rsc)
        self.assertEqual(rsc.get('resource_manager_info').get('id'),
                         test_data.get_fixture_resource_mgr_id)
        self.assertEqual(tuple(rsc.get('inventory').keys()),
                         tuple(test_data.esxcluster_inv_keys))

    def test_resource_delete(self):
        self.client = self._get_fake_client('delete')
        self.assertIsNone(self.client.delete_resource(
            test_data.get_fixture_resource_id))

    def test_resource_activate(self):
        self.client = self._get_fake_client('activate')
        self.assertEqual(self.client.activate_resource(
            test_data.rsc_id, test_data.net_conf_dict),
            test_data.net_conf_dict)

    def test_resource_deactivate(self):
        self.client = self._get_fake_client('deactivate')
        self.assertEqual(self.client.deactivate_resource(
            test_data.rsc_id, test_data.deactivate_forced_dict), {})

    def test_res_template(self):
        type_ = ""
        self.client = self._get_fake_client("get_resource_template")
        self.assertEqual(self.client.get_resource_template(
            type_), None)
