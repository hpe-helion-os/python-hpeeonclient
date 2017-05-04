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


class Eonv2ClientTests(utils.BaseTestCase):
    def setUp(self):
        super(Eonv2ClientTests, self).setUp()
        self.client = self._get_fake_client()

    def _get_fake_client(self):
        return fakes.FakeClient(*test_data.HTTP_ARGS, **test_data.HTTP_KWARGS)

    def test_get_resource_mgr_list_all(self):
        self.client.get_resource_mgr_list(_type=None)
        self.client.assert_called_with(*['GET', 'v2/resource_mgrs', None])

    def test_get_resource_mgr_list_type(self):
        _type = 'vcenter'
        self.client.get_resource_mgr_list(_type=_type)
        url = 'v2/resource_mgrs?type=%s' % _type
        self.client.assert_called_with(*['GET', url, None])

    def test_get_resource_mgr(self):
        self.client.get_resource_mgr(test_data.rsc_mgr_id)
        url = 'v2/resource_mgrs/%s' % test_data.rsc_mgr_id
        self.client.assert_called_with(*['GET', url, None])

    def test_add_resource_mgr(self):
        self.client.add_resource_mgr(test_data.vc_data)
        self.client.assert_called_with(*['POST', 'v2/resource_mgrs/',
                                         test_data.vc_data])

    def test_update_resource_mgr(self):
        self.client.update_resource_mgr(test_data.rsc_mgr_id,
                                        test_data.vc_data1)
        url = 'v2/resource_mgrs/%s' % test_data.rsc_mgr_id
        self.client.assert_called_with(*['PUT', url, test_data.vc_data1])

    def test_delete_resource_mgr(self):
        self.client.delete_resource_mgr(test_data.rsc_mgr_id)
        url = 'v2/resource_mgrs/%s' % test_data.rsc_mgr_id
        self.client.assert_called_with(*['DELETE', url, None])

    def test_get_resource_list_all(self):
        self.client.get_resource_list(_type=None)
        self.client.assert_called_with(*['GET', 'v2/resources', None])

    def test_get_resource_list_type(self):
        _type = 'rhel'
        self.client.get_resource_list(_type=_type)
        url = 'v2/resources?type=%s' % _type
        self.client.assert_called_with(*['GET', url, None])

    def test_get_resource(self):
        self.client.get_resource(test_data.rsc_id)
        url = 'v2/resources/%s' % test_data.rsc_id
        self.client.assert_called_with(*['GET', url, None])

    def test_add_resource(self):
        self.client.add_resource(test_data.rhel_data)
        self.client.assert_called_with(*['POST', 'v2/resources/',
                                         test_data.rhel_data])

    def test_update_resource(self):
        self.client.update_resource(test_data.rsc_id, test_data.rhel_data1)
        url = 'v2/resources/%s' % test_data.rsc_id
        self.client.assert_called_with(*['PUT', url, test_data.rhel_data1])

    def test_delete_resource(self):
        self.client.delete_resource(test_data.rsc_id)
        url = 'v2/resources/%s' % test_data.rsc_id
        self.client.assert_called_with(*['DELETE', url, None])

    def test_activate_resource(self):
        self.client.activate_resource(test_data.rsc_id,
                                      test_data.net_conf_dict)
        url = 'v2/resources/%s/activate/' % test_data.rsc_id
        self.client.assert_called_with(*['POST', url, test_data.net_conf_dict])

    def test_provision_resource(self):
        self.client.provision_resource(test_data.rsc_id,
                                       test_data.net_conf_dict)
        url = 'v2/resources/%s/provision/' % test_data.rsc_id
        self.client.assert_called_with(*['POST', url, test_data.net_conf_dict])

    def test_deactivate_resource(self):
        self.client.deactivate_resource(test_data.rsc_id,
                                        test_data.deactivate_forced_dict)
        url = 'v2/resources/%s/deactivate/' % test_data.rsc_id
        self.client.assert_called_with(*['DELETE', url, None])

    def test_get_resource_template(self):
        type_ = "esxcluster"
        self.client.get_resource_template(type_)
        url = 'v2/resources/%s/get_template/' % type_
        self.client.assert_called_with(*['GET', url, None])

    def tearDown(self):
        super(Eonv2ClientTests, self).tearDown()
