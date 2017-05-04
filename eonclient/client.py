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


from eonclient import exc
from eonclient.common import utils
from eonclient.openstack.common import strutils

import six.moves.urllib.parse as urlparse

from keystoneclient.v2_0 import client as v2_client
from keystoneclient.v3 import client as v3_client


def _adjust_kwargs(kwargs):
    client_kwargs = dict(username=kwargs.get('os_username'),
                         password=kwargs.get('os_password'),
                         tenant_id=kwargs.get('os_tenant_id'),
                         tenant_name=kwargs.get('os_tenant_name'),
                         auth_url=kwargs.get('os_auth_url'),
                         region_name=kwargs.get('os_region_name'),
                         service_type=kwargs.get('os_service_type'),
                         endpoint_type=kwargs.get('os_endpoint_type'),
                         insecure=kwargs.get('os_insecure'),
                         cacert=kwargs.get('os_cacert'),
                         cert_file=kwargs.get('os_cert'),
                         key_file=kwargs.get('os_key'),
                         token=kwargs.get('os_token'),
                         user_domain_name=kwargs.get('os_user_domain_name'),
                         user_domain_id=kwargs.get('os_user_domain_id'),
                         project_domain_name=kwargs.get(
                             'os_project_domain_name'),
                         project_domain_id=kwargs.get('os_project_domain_id'),
                         project_name=kwargs.get('os_project_name'),
                         project_id=kwargs.get('os_project_id'),
                         debug=kwargs.get('debug'))

    timeout = kwargs.get('timeout')
    if timeout is not None:
        timeout = int(timeout)
        if timeout <= 0:
            timeout = None

    insecure = strutils.bool_from_string(kwargs.get('insecure'))
    verify = kwargs.get('verify')
    if verify is None:
        if insecure:
            verify = False
        else:
            verify = client_kwargs.get('os_cacert') or True

    cert = client_kwargs.get('os_cert')
    key = client_kwargs.get('os_key')
    if cert and key:
        cert = cert, key

    client_kwargs.update({'verify': verify, 'cert': cert, 'timeout': timeout})
    return client_kwargs


def _get_ksclient(**kwargs):
    """Get an endpoint and auth token from Keystone.
    """
    url_parts = urlparse.urlparse(kwargs.get('auth_url'))
    (scheme, netloc, path, params, query, fragment) = url_parts
    path = path.lower()
    if path.startswith('/v3'):
        ksclient = v3_client
    elif path.startswith('/v2'):
        ksclient = v2_client
    else:
        raise exc.CommandError('Unable to determine the Keystone '
                               'version to authenticate with '
                               'using the given auth_url.')
    return ksclient.Client(**kwargs)


def _get_endpoint(client, **kwargs):
    """Get an endpoint using the provided keystone client."""
    return client.service_catalog.url_for(
        service_type=kwargs.get('service_type') or 'esx_onboarder',
        endpoint_type=kwargs.get('endpoint_type') or 'publicURL')


def get_client(api_version, **kwargs):
    """Get an authtenticated client, based on the credentials
       in the keyword args.
    """

    if kwargs.get('os_token') and kwargs.get('eon_url'):
        token = kwargs.get('os_token')
        endpoint = kwargs.get('eon_url')
    else:
        client_kwargs = _adjust_kwargs(kwargs)
        _ksclient = _get_ksclient(**client_kwargs)
        token = (kwargs.get('os_token') if kwargs.get('os_token')
                 else _ksclient.auth_token)

        endpoint = (kwargs.get('eon_url') or
                    _get_endpoint(_ksclient, **client_kwargs))

    cli_kwargs = {
        'token': token,
        'insecure': kwargs.get('insecure'),
        'timeout': kwargs.get('timeout'),
        'cacert': kwargs.get('os_cacert'),
        'cert_file': kwargs.get('os_cert'),
        'key_file': kwargs.get('os_key'),
    }

    return Client(api_version, endpoint, **cli_kwargs)


def Client(version, *args, **kwargs):
    module = utils.import_versioned_module(version, 'client')
    client_class = getattr(module, 'Client')
    return client_class(*args, **kwargs)
