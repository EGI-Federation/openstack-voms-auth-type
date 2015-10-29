from __future__ import print_function

import os
import sys

from keystoneclient import session as ksc_session
from keystoneclient.auth import base
from openstackclient.api import auth
from openstackclient.common import clientmanager
from os_client_config import config as cloud_config
from six.moves import urllib


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


def main():
    import argparse
    parser = argparse.ArgumentParser('clientmanager')
    clientmanager.build_plugin_option_parser(parser)
    parser.add_argument(
        '--os-cloud',
        metavar='<cloud-config-name>',
        dest='cloud',
        default=env('OS_CLOUD'),
        help='Cloud name in clouds.yaml (Env: OS_CLOUD)',
    )
    parser.add_argument(
        '--insecure',
        action='store_true',
        dest='insecure',
        help='Disable server certificate verification',
    )
    opts = parser.parse_args()

    cc = cloud_config.OpenStackConfig()
    cloud_opts = cc.get_one_cloud(
        opts.cloud,
        argparse=opts,
    )
    auth_plugin_name = auth.select_auth_plugin(cloud_opts)
    (auth_plugin, auth_params) = auth.build_auth_params(
        auth_plugin_name,
        cloud_opts,
    )
    auth_p = auth_plugin.load_from_options(**auth_params)
    auth_plugin = base.get_plugin_class(auth_plugin_name)

    session = ksc_session.Session(
        auth=auth_p,
        verify=not opts.insecure,
    )

    base_url = auth_params['auth_url']
    if base_url[-1] != '/':
        base_url += '/'
    tenant_url = urllib.parse.urljoin(base_url, 'tenants')
    tenants = session.get(tenant_url)
    for tenant in tenants.json().get('tenants', []):
        print(("Tenant id: %(id)s\n"
               "Tenant name: %(name)s\n"
               "Enabled: %(enabled)s\n"
               "Description: %(description)s\n") % tenant)
    return 0


if __name__ == '__main__':
    sys.exit(main())
