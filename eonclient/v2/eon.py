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

import json
import os

from eonclient.common import utils

FAIL = 'failed'


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


@utils.arg('--type', metavar='<RESOURCE_MANAGER_TYPE>',
           help='(Optional) filter Resource managers based on TYPE.'
                ' vcenter')
@utils.handle_exception
def do_resource_manager_list(ec, args):
    """List Resource Managers (vCenters)."""
    mgr_list = []
    mgrs = ec.get_resource_mgr_list(_type=getattr(args, 'type'))
    for mgr in mgrs:
        mgr_list.append(Struct(**mgr))
    fields = ['id', 'name', 'ip_address', 'type']
    field_labels = ['ID', 'Name', 'IP Address', 'Type']
    utils.print_list(mgr_list, fields, field_labels)


@utils.arg('mgr-id', metavar='<RESOURCE_MANAGER_ID>',
           help='ID of the Resource Manager to display details')
@utils.handle_exception
def do_resource_manager_show(ec, args):
    """Show Resource Manager (vCenter) details."""
    mgr = utils.frame_cli_out(ec.get_resource_mgr(getattr(args, 'mgr-id')))
    utils.sanitize_password(mgr)
    dc_list = []
    clust_list = []
    dc_dict = mgr.get('inventory').get('resources').get('datacenter')
    dc_dict.pop('count')
    for key in dc_dict.keys():
        dc_list.append(dc_dict.get(key).get('name'))
        clust_list = clust_list + dc_dict.get(key).get('clusters').values()
    mgr['Datacenters'] = ', '.join(dc_list)
    mgr['Clusters'] = ', '.join(clust_list)
    mgr['State'] = utils.parse_meta_data(mgr, "state")
    mgr.pop('inventory')
    mgr.pop('meta_data')
    utils.print_dict(mgr)


@utils.arg('vcenter-id', metavar='<VCENTER_ID>',
           help='ID of the vcenter to get the password')
def do_get_vcenter_password(ec, args):
    """Get Resource Manager (vCenter) password."""
    vc = ec.get_resource_mgr(getattr(args, 'vcenter-id'))
    print vc.get('password')


@utils.arg('--name', metavar='<RESOURCE_MANAGER_NAME>',
           help='Name of the Resource Manager to be added')
@utils.arg('--ip-address', metavar='<RESOURCE_MANAGER_IP_ADDR>', required=True,
           help='IP address of the Resource Manager to be added')
@utils.arg('--username', metavar='<RESOURCE_MANAGER_USERNAME>', required=True,
           help='Username of the Resource Manager administrator')
@utils.arg('--password', metavar='<RESOURCE_MANAGER_PASSWORD>', required=True,
           help='Password of the Resource Manager administrator')
@utils.arg('--port', metavar='<RESOURCE_MANAGER_PORT>',
           help='Port of the Resource Manager to be added')
@utils.arg('--type', metavar='<RESOURCE_MANAGER_TYPE>', required=True,
           help='Type of the Resource Manager to be added. vcenter')
@utils.handle_exception
def do_resource_manager_add(ec, args):
    """Add Resource Manager (vCenter)"""
    required_fields = ['name', 'ip_address', 'username',
                       'password', 'port', 'type']
    fields = dict(
        filter(lambda x: x[1] is not None and x[0] in required_fields,
               vars(args).items()))
    mgr = utils.frame_cli_out(ec.add_resource_mgr(fields))
    utils.sanitize_password(mgr)
    mgr['State'] = utils.parse_meta_data(mgr, "state")
    mgr.pop('meta_data')
    utils.print_dict(mgr)


@utils.arg('rsc-id', metavar='<RESOURCE_ID>',
           help='ID of the Resource to provision')
@utils.arg('--type', metavar='<RESOURCE_TYPE>', required=True,
           help='Type of the Resource to be provisioned')
@utils.arg('--os-version', metavar='<OS_PROFILE_VERSION>',
           help='OS profile version to use for provision')
@utils.arg('--boot-from-san', metavar='<BOOT-FROM-SAN-ENABLED>',
           help='For provisioning compute node with san boot enabled')
@utils.arg('--property', metavar="<key=value>", action='append', default=[],
           help=("Arbitrary property to associate with any eon resource. "
                 "May be used multiple times."))
@utils.handle_exception
def do_resource_provision(ec, args):
    """Baremetal provisioning of a Resource (HLINUX KVM/RHEL KVM)"""
    required_fields = ['type', 'os_version', 'boot_from_san', 'property']
    data = dict(
        filter(lambda x: x[1] is not None and x[0] in required_fields,
               vars(args).items()))
    rsc = ec.provision_resource(getattr(args, 'rsc-id'), data)
    utils.sanitize_password(rsc)
    utils.print_dict(rsc, wrap=100)


@utils.arg('--ip-address', metavar='<RESOURCE_MANAGER_IP_ADDR>',
           help='IP address of the Resource Manager to be updated')
@utils.arg('--username', metavar='<RESOURCE_MANAGER_USERNAME>',
           help='Username of the Resource Manager administrator to be updated')
@utils.arg('--password', metavar='<RESOURCE_MANAGER_PASSWORD>',
           help='Password of the Resource Manager administrator to be updated')
@utils.arg('--port', metavar='<RESOURCE_MANAGER_PORT>',
           help='Port of the Resource Manager to be updated')
@utils.arg('mgr-id', metavar='<RESOURCE_MANAGER_ID>',
           help='ID of the Resource Manager to be updated')
@utils.handle_exception
def do_resource_manager_update(ec, args):
    """Update Resource Manager (vCenter) details"""
    update_fields = ['ip_address', 'username', 'port', 'password']
    update_data = {fl: getattr(args, fl) for fl in update_fields
                   if getattr(args, fl) is not None}
    mgr = utils.frame_cli_out(ec.update_resource_mgr(getattr(args, 'mgr-id'),
                                                     update_data))
    mgr['State'] = utils.parse_meta_data(mgr, "state")
    mgr.pop('meta_data')
    utils.sanitize_password(mgr)
    utils.print_dict(mgr)


@utils.arg('mgr-id', metavar='<RESOURCE_MANAGER_ID>',
           help='ID of the Resource Manager to be deleted')
@utils.handle_exception
def do_resource_manager_delete(ec, args):
    """Delete Resource Manager (vCenter)."""
    ec.delete_resource_mgr(getattr(args, 'mgr-id'))


@utils.arg('--type', metavar='<RESOURCE_TYPE>',
           help='(Optional) filter Resources based on TYPE.'
                ' esxcluster (or) rhel (or) hlinux')
@utils.arg('--state', metavar='<RESOURCE_STATE>',
           help='(Optional) filter Resources based on STATE.'
                ' imported (or) provisioned (or) activated')
@utils.arg('--manager-id', metavar='<RESOURCE_MANAGER_ID>',
           help='(Optional) filter Resources based on Resource Manager')
@utils.arg('--list-supported-types', metavar='<true>',
           help='(Optional) filter which returns all the supported types')
@utils.handle_exception
def do_resource_list(ec, args):
    """List Resources (ESX cluster/HLINUX KVM/RHEL KVM/Hyper-V)."""
    rsc_list = []
    mgr_id = getattr(args, 'manager_id')
    list_supported_types = getattr(args, 'list_supported_types')

    if list_supported_types:
        supported_types = ec.get_resource_list(
            list_supported_types=list_supported_types)
        d = {"supported_types": supported_types}
        utils.print_dict(d)
        return

    rscs_list = ec.get_resource_list(_type=getattr(args, 'type'),
                                     state=getattr(args, 'state'))
    if not mgr_id:
        rscs = rscs_list
    else:
        rscs = [item for item in rscs_list
                if item.get('resource_mgr_id') == mgr_id]

    for rsc in rscs:
        moid = [item.get('value')
                for item in rsc.get('meta_data')
                if item.get('name') == 'cluster_moid']
        if moid:
            rsc['moid'] = moid[0]
        rsc_list.append(Struct(**rsc))

    fields = ['id', 'name', 'moid', 'resource_mgr_id',
              'ip_address', 'port', 'type', 'state']
    field_labels = ['ID', 'Name', 'Moid', 'Resource Manager ID',
                    'IP Address', 'Port', 'Type', 'State']
    utils.print_list(rsc_list, fields, field_labels)


@utils.arg('rsc-id', metavar='<RESOURCE_ID>',
           help='ID of the Resource to display details')
@utils.handle_exception
def do_resource_show(ec, args):
    """Show Resource (ESX cluster/HLINUX KVM/RHEL KVM/Hyper-V) details."""
    rsc = utils.frame_cli_out(ec.get_resource(getattr(args, 'rsc-id')))
    utils.sanitize_password(rsc)
    moid = [item.get('value') for item in rsc.get('meta_data')
            if item.get('name') == 'cluster_moid']
    if moid:
        rsc['Resource Moid'] = moid[0]
    hlm_prop = [item.get('value') for item in rsc.get('meta_data')
                if item.get('name') == 'hlm_properties']
    if hlm_prop:
        rsc['HLM-PROPERTIES'] = hlm_prop[0]

    if rsc.get("Type") == "esxcluster":
        inv = rsc.pop('inventory')
        rsc['Datacenter Name'] = inv.get('datacenter').get('name')
        rsc['Datacenter Moid'] = inv.get('datacenter').get('moid')
        hosts = inv.get('hosts')
        rsc['Host Names'] = ', '.join([host.get('name') for host in hosts])
        rsc['Host Moids'] = ', '.join([host.get('moid') for host in hosts])
    else:
        meta_data_map = {'ilo_ip': 'ILO Ip',
                         'mac_addr': 'Mac Address',
                         'ilo_user': 'ILO User',
                         'ilo_password': 'ILO Password',
                         'hypervisor_id': 'Nova Hypervisor Id'}
        inv = rsc.pop('meta_data')
        for item in inv:
            if item.get('name') != 'ilo_password':
                rsc[meta_data_map[item.get('name')]] = item.get('value')
            else:
                rsc[meta_data_map[item.get('name')]] = "<SANITIZED>"

    rsc.pop('resource_manager_info', None)
    rsc.pop('meta_data', None)
    utils.print_dict(rsc, wrap=100)


@utils.arg('--type', metavar='<RESOURCE_TYPE>', required=True,
           help='Type of the Resource to be added.'
                ' esxcluster (or) rhel (or) hlinux (or) baremetal')
@utils.arg('--name', metavar='<RESOURCE_NAME>', required=True,
           help='Name of the Resource to be added')
@utils.arg('--ip-address', metavar='<RESOURCE_IP_ADDR>', required=True,
           help='IP address of the Resource to be added')
@utils.arg('--username', metavar='<RESOURCE_USERNAME>', required=True,
           help='Username of the Resource administrator')
@utils.arg('--password', metavar='<RESOURCE_PASSWORD>', required=True,
           help='Password of the Resource administrator')
@utils.arg('--port', metavar='<RESOURCE_PORT>', required=False,
           help='Port of the Resource to be added')
@utils.arg('--ilo-ip', metavar='<ILO_IP>', required=False,
           help='ILO IP of the baremetal node')
@utils.arg('--ilo-password', metavar='<ILO_PASSWORD>', required=False,
           help='ILO Password of baremetal node')
@utils.arg('--mac-addr', metavar='<MAC_ADDRESS>', required=False,
           help='Mac Address of baremetal node for conf network')
@utils.arg('--ilo-user', metavar='<ILO_USER>', required=False,
           help='ILO User of baremetal node')
@utils.handle_exception
def do_resource_add(ec, args):
    """Add Resource (HLINUX KVM/RHEL KVM/Hyper-V)"""
    # NO resource add for EsxCluster, auto-import happens
    required_fields = ['name', 'ip_address', 'username',
                       'password', 'port', 'type']
    fields = dict(
        filter(lambda x: x[1] is not None and x[0] in required_fields,
               vars(args).items()))
    if args.type == 'baremetal':
        ex_fields = _do_resource_add_baremetal(args)
        fields.update(ex_fields)
    # TODO(juigil): No resource add for esxclusters. Required for kvm, hyperv
    rsc = ec.add_resource(fields)
    rsc = utils.frame_cli_out(rsc)
    utils.sanitize_password(rsc, meta_data=True)
    utils.print_dict(rsc, wrap=100)


@utils.handle_exception
def _do_resource_add_baremetal(args):
    """Add Baremetal Resource (HLINUX KVM/RHEL KVM)"""
    required_fields = ['ilo_ip', 'ilo_password', 'ilo_user', 'mac_addr']
    fields = dict(
        filter(lambda x: x[1] is not None and x[0] in required_fields,
               vars(args).items()))
    return fields


@utils.arg('--server-group', metavar='<Server-Group-Name>',
           help='pass the name of the server group. '
                'valid for only esxclusters'
                ' for host commissioning')
@utils.arg('--action', metavar='<add_host>',
           help='valid for only esxclusters'
           ' for host commissioning')
@utils.arg('--name', metavar='<RESOURCE_NAME>',
           help='Name of the Resource to be updated')
@utils.arg('--ip-address', metavar='<RESOURCE_IP_ADDR>',
           help='IP address of the Resource to be updated')
@utils.arg('--username', metavar='<RESOURCE_USERNAME>',
           help='Username of the Resource administrator')
@utils.arg('--password', metavar='<RESOURCE_PASSWORD>',
           help='Password of the Resource administrator')
@utils.arg('--port', metavar='<RESOURCE_PORT>',
           help='Port of the Resource to be updated')
@utils.arg('rsc-id', metavar='<RESOURCE_ID>',
           help='ID of the Resource to be updated')
@utils.arg('--ilo-ip', metavar='<ILO_IP>', required=False,
           help='ILO IP of the baremetal node to be updated')
@utils.arg('--ilo-password', metavar='<ILO_PASSWORD>', required=False,
           help='ILO Password of baremetal node to be updated')
@utils.arg('--mac-addr', metavar='<MAC_ADDRESS>', required=False,
           help='Mac Address of baremetal node for conf network to be updated')
@utils.arg('--ilo-user', metavar='<ILO_USER>', required=False,
           help='ILO User of baremetal node to be updated')
@utils.handle_exception
def do_resource_update(ec, args):
    """Update Resource Manager (vCenter) details"""
    update_fields = ['name', 'ip_address', 'username', 'port',
                     'action', 'server_group', 'password']
    if getattr(args, 'server_group'):
        if not args.action:
            print("Error: Server_group can only be passed if action"
                  " parameter is used")
            exit(1)

    update_data = {fl: getattr(args, fl) for fl in update_fields
                   if getattr(args, fl) is not None}
    update_data.update(_do_resource_update_baremetal(args))
    response, rsc = ec.update_resource(getattr(args, 'rsc-id'), update_data)
    utils.sanitize_password(rsc, meta_data=True)
    utils.print_dict(rsc, wrap=100)


@utils.handle_exception
def _do_resource_update_baremetal(args):
    required_fields = ['ilo_ip', 'ilo_password', 'ilo_user', 'mac_addr']
    return {fl: getattr(args, fl) for fl in required_fields
            if getattr(args, fl) is not None}


@utils.arg('rsc-id', metavar='<RESOURCE_ID>',
           help='ID of the Resource to be deleted')
@utils.handle_exception
def do_resource_delete(ec, args):
    """Delete Resource (HLINUX KVM/RHEL KVM/Hyper-V)."""
    # No resource delete for esxcluster. Even when deleted eon imports the
    # cluster back
    try:
        ec.delete_resource(getattr(args, 'rsc-id'))
    except Exception as e:
        print("Unable to delete the Resource %s."
              " An unknown exception %s occured" %
              (getattr(args, 'rsc-id'), e.message))


@utils.arg('rsc-id', metavar='<RESOURCE_ID>',
           help='ID of the Resource to be activated')
@utils.arg('--config-json', metavar='<NETWORK_JSON>', required=True,
           help='network configuration json file location')
@utils.handle_exception
def do_resource_activate(ec, args):
    """Activate Resource (ESX cluster/HLINUX KVM/RHEL KVM/Hyper-V)."""
    data = dict()
    config_json_path = getattr(args, 'config_json')
    if config_json_path:
        with open(config_json_path) as cj:
            config_json = ''.join([line.strip() for line in cj
                                   if '#' not in line.strip()])
            data = json.loads(config_json)
    activate_out = ec.activate_resource(getattr(args, 'rsc-id'), data)
    utils.sanitize_password(activate_out, meta_data=False)
    utils.print_dict(activate_out, wrap=100)


@utils.arg('rsc-id', metavar='<RESOURCE_ID>',
           help='ID of the Resource to be deactivated')
@utils.arg('--forced', metavar='<FORCED_DEACTIVATE>',
           help='forced deactivate (true/false). Defaults to False')
@utils.handle_exception
def do_resource_deactivate(ec, args):
    """Deactivate Resource (ESX cluster/HLINUX KVM/RHEL KVM/Hyper-V)."""
    forced = getattr(args, 'forced')
    data = {'forced': False}
    if forced:
        if forced.lower() == 'true':
            data.update({'forced': True})
    deactivate_out = ec.deactivate_resource(getattr(args, 'rsc-id'), data)
    utils.sanitize_password(deactivate_out, meta_data=False)
    utils.print_dict(deactivate_out, wrap=100)


@utils.arg('--filename', metavar='<Activate JSON>', required=False,
           help='filename to store activation configuration template json')
@utils.arg('--type', metavar='<Type of the resource>', required=True,
           help='Resource type like "esxcluster"')
@utils.arg('--input-json', metavar='<NETWORK_JSON>',
           help='input data to populate network configuration')
@utils.handle_exception
def do_get_activation_template(ec, args):
    """
    Get activation template json for ESX cluster/HLINUX KVM/RHEL KVM/Hyper-V.
    """
    filename = getattr(args, 'filename')
    if not filename:
        filename = "activate-template.json"
    data = dict()
    config_json_path = getattr(args, 'input_json')
    if config_json_path:
        with open(config_json_path) as cj:
            config_json = ''.join([line.strip() for line in cj
                                   if '#' not in line.strip()])
            data = json.loads(config_json)
    activate_json = ec.get_resource_template(getattr(args, "type"), data)

    file_path = os.path.expanduser('~')
    file_path = file_path + "/" + filename
    with open(file_path, 'w') as template:
        json.dump(activate_json, template, indent=1)

    print '-' * 63
    print "Saved the sample network file in %s" % file_path
    print '-' * 63
