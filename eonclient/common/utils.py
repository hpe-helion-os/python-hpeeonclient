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


from __future__ import print_function
import itertools
import os
import six
import sys
import textwrap
import uuid

import prettytable
from functools import wraps

from eonclient import exc
from eonclient.openstack.common import cliutils
from eonclient.openstack.common import importutils
from eonclient.openstack.common import strutils

api_key_mapping = {
    'id': 'ID',
    'ip_address': 'IPv4Address',
    'name': 'Name',
    'password': 'Password',
    'port': 'Port',
    'type': 'Type',
    'username': 'Username',
    'state': 'State',
    'resource_mgr_id': 'Resource Manager ID'
}

SANITIZE_PASSWORDS = ["password", "ilo_password"]


# Decorator for cli-args
def arg(*args, **kwargs):
    def _decorator(func):
        if 'help' in kwargs:
            if 'default' in kwargs:
                kwargs['help'] += " Defaults to %s." % kwargs['default']
            required = kwargs.get('required', False)
            if required:
                kwargs['help'] += " [Required]."

        # Because of the sematics of decorator composition if we just append
        # to the options list positional options will appear to be backwards.
        func.__dict__.setdefault('arguments', []).insert(0, (args, kwargs))
        return func
    return _decorator


def pretty_choice_list(l):
    return ', '.join("'%s'" % i for i in l)


def print_list(objs, fields, field_labels, formatters={}, sortby=0):

    def _make_default_formatter(field):
        return lambda o: getattr(o, field, '')

    new_formatters = {}
    for field, field_label in itertools.izip(fields, field_labels):
        if field in formatters:
            new_formatters[field_label] = formatters[field]
        else:
            new_formatters[field_label] = _make_default_formatter(field)

    cliutils.print_list(objs, field_labels,
                        formatters=new_formatters,
                        sortby_index=sortby)


def parse_meta_data(response, key):
    """
    :return an value of @key requested
    """
    return [item.get('value')
            for item in response.get('meta_data') or []
            if item.get('name') == key][0]


def print_dict(d, dict_property="Property", wrap=0):
    pt = prettytable.PrettyTable([dict_property, 'Value'],
                                 caching=False, print_empty=False)
    pt.align = 'l'
    for k, v in sorted(six.iteritems(d)):
        # convert dict to str to check length
        if isinstance(v, dict):
            v = str(v)
        if isinstance(v, six.string_types):
            v = strutils.safe_encode(v)
        # if value has a newline, add in multiple rows
        # e.g. fault with stacktrace
        if v and isinstance(v, six.string_types) and r'\n' in v:
            lines = v.strip().split(r'\n')
            col1 = k
            for line in lines:
                if wrap > 0:
                    line = textwrap.fill(str(line), wrap)
                pt.add_row([col1, line])
                col1 = ''
        else:
            if wrap > 0:
                v = textwrap.fill(str(v), wrap)
            pt.add_row([k, v])
    print(pt.get_string())


def find_resource(manager, name_or_id):
    """Helper for the _find_* methods."""
    # first try to get entity as integer id
    try:
        if isinstance(name_or_id, int) or name_or_id.isdigit():
            return manager.get(int(name_or_id))
    except exc.NotFound:
        pass

    # now try to get entity as uuid
    try:
        uuid.UUID(str(name_or_id))
        return manager.get(name_or_id)
    except (ValueError, exc.NotFound):
        pass

    # finally try to find entity by name
    try:
        return manager.find(name=name_or_id)
    except exc.NotFound:
        msg = "No %s with a name or ID of '%s' exists." % \
              (manager.resource_class.__name__.lower(), name_or_id)
        raise exc.CommandError(msg)


def string_to_bool(arg):
    return arg.strip().lower() in ('t', 'true', 'yes', '1')


def env(*vars, **kwargs):
    """Search for the first defined of possibly many env vars

    Returns the first environment variable defined in vars, or
    returns the default defined in kwargs.
    """
    for v in vars:
        value = os.environ.get(v, None)
        if value:
            return value
    return kwargs.get('default', '')


def import_versioned_module(version, submodule=None):
    module = 'eonclient.v%s' % version
    if submodule:
        module = '.'.join((module, submodule))
    return importutils.import_module(module)


def args_array_to_dict(kwargs, key_to_convert):
    values_to_convert = kwargs.get(key_to_convert)
    if values_to_convert:
        try:
            kwargs[key_to_convert] = dict(v.split("=", 1)
                                          for v in values_to_convert)
        except ValueError:
            raise exc.CommandError(
                '%s must be a list of key=value not "%s"' % (
                    key_to_convert, values_to_convert))
    return kwargs


def key_with_slash_to_nested_dict(kwargs):
    nested_kwargs = {}
    for k in list(kwargs):
        keys = k.split('/', 1)
        if len(keys) == 2:
            nested_kwargs.setdefault(keys[0], {})[keys[1]] = kwargs[k]
            del kwargs[k]
    kwargs.update(nested_kwargs)
    return kwargs


def merge_nested_dict(dest, source, depth=0):
    for (key, value) in six.iteritems(source):
        if isinstance(value, dict) and depth:
            merge_nested_dict(dest[key], value,
                              depth=(depth - 1))
        else:
            dest[key] = value


def exit(msg=''):
    if msg:
        print(msg, file=sys.stderr)
    sys.exit(1)


def frame_cli_out(data):
    for k, v in api_key_mapping.iteritems():
        val = data.get(k)
        if val:
            if val == 'UNSET':
                data.pop(k)
            else:
                data[v] = data.pop(k)
    return data


def sanitize_password(item, meta_data=False):
    for key in SANITIZE_PASSWORDS:
        item.pop(key) if item.get(key) else None
        item['Password'] = '<SANITIZED>'
    if meta_data:
        data = item.get("meta_data") or []
        for meta in data:
            if meta.get("name") in SANITIZE_PASSWORDS:
                meta['value'] = '<SANITIZED>'


def handle_exception(fn):
    """Helper to handle exception gracefully"""
    @wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            try:
                print (e.details)
            except:
                print (e)

    return wrapped