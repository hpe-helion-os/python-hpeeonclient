#!/usr/bin/python
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


"""
Command-line interface to the HP EON API.
"""

from __future__ import print_function

import argparse
import logging
import sys
import six

import eonclient
from eonclient import client as eon_client
from eonclient.common import utils
from eonclient import exc
from eonclient.openstack.common import cliutils
from eonclient.openstack.common import strutils


class EonShell(object):

    def _append_global_identity_args(self, parser):
        # TODO: these are global identity (Keystone) arguments which
        # should be consistent and shared by all service clients. Therefore,
        # they should be provided by python-keystoneclient. We will need to
        # refactor this code once this functionality is available in
        # python-keystoneclient.

        parser.add_argument(
            '--os-auth-strategy', metavar='<auth-strategy>',
            default=cliutils.env('OS_AUTH_STRATEGY', default='keystone'),
            help='Authentication strategy (Env: OS_AUTH_STRATEGY,'
                 ' default keystone). For now, any other value will disable'
                 ' the authentication')
        parser.add_argument(
            '--os_auth_strategy',
            help=argparse.SUPPRESS)

        parser.add_argument('--os-username',
                            metavar='<auth-user-name>',
                            default=cliutils.env('OS_USERNAME'),
                            help='OpenStack user name. '
                            'Default=env[OS_USERNAME].')
        parser.add_argument('--os_username',
                            help=argparse.SUPPRESS)

        parser.add_argument('--os-password',
                            metavar='<auth-password>',
                            default=cliutils.env('OS_PASSWORD'),
                            help='Password for OpenStack user. '
                            'Default=env[OS_PASSWORD].')
        parser.add_argument('--os_password',
                            help=argparse.SUPPRESS)

        parser.add_argument('--os-tenant-name',
                            metavar='<auth-tenant-name>',
                            default=cliutils.env('OS_TENANT_NAME'),
                            help='Tenant name. '
                            'Default=env[OS_TENANT_NAME].')
        parser.add_argument('--os_tenant_name',
                            help=argparse.SUPPRESS)

        parser.add_argument('--os-tenant-id',
                            metavar='<auth-tenant-id>',
                            default=cliutils.env('OS_TENANT_ID'),
                            help='ID for the tenant. '
                            'Default=env[OS_TENANT_ID].')
        parser.add_argument('--os_tenant_id',
                            help=argparse.SUPPRESS)

        parser.add_argument('--os-auth-url',
                            metavar='<auth-url>',
                            default=cliutils.env('OS_AUTH_URL'),
                            help='URL for the authentication service. '
                            'Default=env[OS_AUTH_URL].')
        parser.add_argument('--os_auth_url',
                            help=argparse.SUPPRESS)

        parser.add_argument(
            '--os-user-id', metavar='<auth-user-id>',
            default=cliutils.env('OS_USER_ID'),
            help='Authentication user ID (Env: OS_USER_ID)')

        parser.add_argument(
            '--os_user_id',
            help=argparse.SUPPRESS)

        parser.add_argument(
            '--os-user-domain-id',
            metavar='<auth-user-domain-id>',
            default=cliutils.env('OS_USER_DOMAIN_ID'),
            help='OpenStack user domain ID. '
            'Defaults to env[OS_USER_DOMAIN_ID].')

        parser.add_argument(
            '--os_user_domain_id',
            help=argparse.SUPPRESS)

        parser.add_argument(
            '--os-user-domain-name',
            metavar='<auth-user-domain-name>',
            default=cliutils.env('OS_USER_DOMAIN_NAME'),
            help='OpenStack user domain name. '
                 'Defaults to env[OS_USER_DOMAIN_NAME].')

        parser.add_argument(
            '--os_user_domain_name',
            help=argparse.SUPPRESS)

        parser.add_argument(
            '--os-project-id',
            metavar='<auth-project-id>',
            default=cliutils.env('OS_PROJECT_ID'),
            help='Another way to specify tenant ID. '
            'This option is mutually exclusive with '
            ' --os-tenant-id. '
            'Defaults to env[OS_PROJECT_ID].')

        parser.add_argument(
            '--os_project_id',
            help=argparse.SUPPRESS)

        parser.add_argument(
            '--os-project-name',
            metavar='<auth-project-name>',
            default=cliutils.env('OS_PROJECT_NAME'),
            help='Another way to specify tenant name. '
                 'This option is mutually exclusive with '
                 ' --os-tenant-name. '
                 'Defaults to env[OS_PROJECT_NAME].')

        parser.add_argument(
            '--os_project_name',
            help=argparse.SUPPRESS)

        parser.add_argument(
            '--os-project-domain-id',
            metavar='<auth-project-domain-id>',
            default=cliutils.env('OS_PROJECT_DOMAIN_ID'),
            help='Defaults to env[OS_PROJECT_DOMAIN_ID].')

        parser.add_argument(
            '--os-project-domain-name',
            metavar='<auth-project-domain-name>',
            default=cliutils.env('OS_PROJECT_DOMAIN_NAME'),
            help='Defaults to env[OS_PROJECT_DOMAIN_NAME].')

        parser.add_argument(
            '--os-cert',
            metavar='<certificate>',
            default=cliutils.env('OS_CERT'),
            help='Defaults to env[OS_CERT].')

        parser.add_argument(
            '--os-key',
            metavar='<key>',
            default=cliutils.env('OS_KEY'),
            help='Defaults to env[OS_KEY].')

        parser.add_argument('--os-region-name',
                            metavar='<region-name>',
                            default=cliutils.env('OS_REGION_NAME',
                                                 'CINDER_REGION_NAME'),
                            help='Region name. '
                            'Default=env[OS_REGION_NAME].')
        parser.add_argument('--os_region_name',
                            help=argparse.SUPPRESS)

        parser.add_argument(
            '--os-token', metavar='<token>',
            default=cliutils.env('OS_TOKEN'),
            help='Defaults to env[OS_TOKEN]')
        parser.add_argument(
            '--os_token',
            help=argparse.SUPPRESS)

        parser.add_argument(
            '--os-url', metavar='<url>',
            default=cliutils.env('OS_URL'),
            help='Defaults to env[OS_URL]')
        parser.add_argument(
            '--os_url',
            help=argparse.SUPPRESS)

        parser.add_argument(
            '--os-cacert',
            metavar='<ca-certificate>',
            default=cliutils.env('OS_CACERT', default=None),
            help="Specify a CA bundle file to use in verifying a TLS (https) "
                 "server certificate. Defaults to env[OS_CACERT]")

        parser.add_argument(
            '--insecure', default=False, action='store_true',
            help='Explicitly allow client to perform "insecure" TLS'
                 '(https) requests. The server\'s certificate will'
                 'not be verified against any certificate'
                 'authorities. This option should be used with caution')

    def get_base_parser(self):
        parser = argparse.ArgumentParser(
            prog='eon',
            description=__doc__.strip(),
            epilog='See "eon help COMMAND" '
                   'for help on a specific command.',
            add_help=False,
            formatter_class=HelpFormatter,
        )

        # Global arguments
        parser.add_argument('-h', '--help',
                            action='store_true',
                            help=argparse.SUPPRESS,
                            )

        parser.add_argument('--version',
                            action='version',
                            version=eonclient.__version__)

        parser.add_argument('-d', '--debug',
                            default=bool(cliutils.env('EONCLIENT_DEBUG')
                                         ),
                            action='store_true',
                            help='Defaults to env[EONCLIENT_DEBUG].')

        parser.add_argument('--timeout',
                            default=600,
                            help='Number of seconds to wait for a response.')
        parser.add_argument('--eon-url',
                            default=cliutils.env('EON_URL'),
                            help='Defaults to env[EON_URL].')

        parser.add_argument('--eon_url',
                            help=argparse.SUPPRESS)

        parser.add_argument('--eon-api-version',
                            default=cliutils.env('EON_API_VERSION',
                                                 default='2'),
                            help='Defaults to env[EON_API_VERSION] '
                            'or 1')

        parser.add_argument('--eon_api_version',
                            help=argparse.SUPPRESS)

        parser.add_argument('--os-service-type',
                            default=cliutils.env('OS_SERVICE_TYPE'),
                            help='Defaults to env[OS_SERVICE_TYPE].')

        parser.add_argument('--os_service_type',
                            help=argparse.SUPPRESS)

        parser.add_argument('--os-endpoint-type',
                            default=cliutils.env('OS_ENDPOINT_TYPE'),
                            help='Defaults to env[OS_ENDPOINT_TYPE].')

        parser.add_argument('--os_endpoint_type',
                            help=argparse.SUPPRESS)

        self._append_global_identity_args(parser)
        return parser

    def get_subcommand_parser(self, version):
        parser = self.get_base_parser()

        self.subcommands = {}
        subparsers = parser.add_subparsers(metavar='<subcommand>')
        submodule = utils.import_versioned_module(version, 'eon')
        self._find_actions(subparsers, submodule)
        self._find_actions(subparsers, self)
        self._add_bash_completion_subparser(subparsers)

        return parser

    def _add_bash_completion_subparser(self, subparsers):
        subparser = subparsers.add_parser(
            'bash_completion',
            add_help=False,
            formatter_class=HelpFormatter
        )
        self.subcommands['bash_completion'] = subparser
        subparser.set_defaults(func=self.do_bash_completion)

    def _find_actions(self, subparsers, actions_module):
        for attr in (a for a in dir(actions_module) if a.startswith('do_')):
            # I prefer to be hypen-separated instead of underscores.
            command = attr[3:].replace('_', '-')
            callback = getattr(actions_module, attr)
            desc = callback.__doc__ or ''
            help = desc.strip().split('\n')[0]
            arguments = getattr(callback, 'arguments', [])

            subparser = subparsers.add_parser(command, help=help,
                                              description=desc,
                                              add_help=False,
                                              formatter_class=HelpFormatter)
            subparser.add_argument('-h', '--help', action='help',
                                   help=argparse.SUPPRESS)
            self.subcommands[command] = subparser
            positional_group = subparser.add_argument_group(
                title='Positional Arguments')
            additional_group = subparser.add_argument_group(title='Options')
            for (args, kwargs) in arguments:
                if args[0].startswith('--'):
                    additional_group.add_argument(*args, **kwargs)
                else:
                    positional_group.add_argument(*args, **kwargs)
            subparser.set_defaults(func=callback)

    def _setup_logging(self, debug):
        format = '%(levelname)s (%(module)s:%(lineno)d) %(message)s'
        if debug:
            logging.basicConfig(format=format, level=logging.DEBUG)
        else:
            logging.basicConfig(format=format, level=logging.WARN)

    def parse_args(self, argv):
        # Parse args once to find version
        parser = self.get_base_parser()
        (options, args) = parser.parse_known_args(argv)
        self._setup_logging(options.debug)

        # build available subcommands based on version
        api_version = options.eon_api_version
        subcommand_parser = self.get_subcommand_parser(api_version)
        self.parser = subcommand_parser

        # Handle top-level --help/-h before attempting to parse
        # a command off the command line
        if options.help or not argv:
            self.do_help(options)
            return 0

        # Return parsed args
        return api_version, subcommand_parser.parse_args(argv)

    def main(self, argv):
        parsed = self.parse_args(argv)
        if parsed == 0:
            return 0
        api_version, args = parsed

        # Short-circuit and deal with help command right away.
        if args.func == self.do_help:
            self.do_help(args)
            return 0
        elif args.func == self.do_bash_completion:
            self.do_bash_completion(args)
            return 0
        if not (args.os_token and args.eon_url):
            if not args.os_username:
                raise exc.CommandError("You must provide a username via "
                                       "either --os-username or via "
                                       "env[OS_USERNAME]")

            if not args.os_password:
                raise exc.CommandError("You must provide a password via "
                                       "either --os-password or via "
                                       "env[OS_PASSWORD]")

            if not args.os_auth_url:
                raise exc.CommandError("You must provide an auth url via"
                                       " either --os-auth-url or via"
                                       " env[OS_AUTH_URL]")
            # V3 stuff
            project_info = (
                args.os_tenant_name or args.os_tenant_id or (
                    args.os_project_name and (
                        args.os_project_domain_name or
                        args.os_project_domain_id
                    )
                ) or args.os_project_id
            )
            if not project_info:
                raise exc.CommandError(
                    "You must provide a tenant_name or tenant_id (for v2.0)"
                    "project_id or project_name (with project_domain_name or"
                    " project_domain_id) (for keystone version v3) via "
                    "  --os-tenant-name (env[OS_TENANT_NAME]),"
                    "  --os-tenant-id (env[OS_TENANT_ID]),"
                    "  --os-project-id (env[OS_PROJECT_ID])"
                    "  --os-project-name (env[OS_PROJECT_NAME]),"
                    "  --os-project-domain-id (env[OS_PROJECT_DOMAIN_ID])"
                    "  --os-project-domain-name (env[OS_PROJECT_DOMAIN_NAME])")

        client = eon_client.get_client(api_version, **(args.__dict__))

        # call whatever callback was selected
        try:
            args.func(client, args)
        except exc.Unauthorized:
            raise exc.CommandError("Invalid OpenStack Identity credentials.")

    def do_bash_completion(self, args):
        """Prints all of the commands and options to stdout.

        The eon.bash_completion script doesn't have to hard code them.
        """
        commands = set()
        options = set()
        for sc_str, sc in self.subcommands.items():
            commands.add(sc_str)
            for option in list(sc._optionals._option_string_actions):
                options.add(option)

        commands.remove('bash-completion')
        commands.remove('bash_completion')
        print(' '.join(commands | options))

    @utils.arg('command', metavar='<subcommand>', nargs='?',
               help='Display help for <subcommand>')
    def do_help(self, args):
        """Display help about this program or one of its subcommands."""
        if getattr(args, 'command', None):
            if args.command in self.subcommands:
                self.subcommands[args.command].print_help()
            else:
                raise exc.CommandError("'%s' is not a valid subcommand" %
                                       args.command)
        else:
            self.parser.print_help()


class HelpFormatter(argparse.HelpFormatter):
    def start_section(self, heading):
        # Title-case the headings
        heading = '%s%s' % (heading[0].upper(), heading[1:])
        super(HelpFormatter, self).start_section(heading)


def main(args=None):
    try:
        if args is None:
            args = sys.argv[1:]

        EonShell().main(args)

    except Exception as e:
        if '--debug' in args or '-d' in args:
            raise
        else:
            print(strutils.safe_encode(six.text_type(e)), file=sys.stderr)
        sys.exit(1)