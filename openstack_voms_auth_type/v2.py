# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2015 Spanish National Research Council
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

from keystoneauth1 import loading
from keystoneauth1.identity import v2
from positional import positional

import utils

class VomsV2AuthPlugin(v2.Auth):
    @positional()
    def __init__(self, x509_user_proxy=None, **kwargs):
        # remove v2 auth not valid args
        if 'project_id' in kwargs:
            kwargs['tenant_id'] = kwargs['project_id']
            del kwargs['project_id']
        if 'project_name' in kwargs:
            kwargs['tenant_name'] = kwargs['project_name']
            del kwargs['project_name']
        super(VomsV2AuthPlugin, self).__init__(**kwargs)
        self.x509_user_proxy = x509_user_proxy

    def get_auth_data(self, headers=None):
        return {'voms': True}

    def get_auth_ref(self, session, **kwargs):
        with utils.BundleBuilder(session, self.x509_user_proxy) as p:
            return super(VomsV2AuthPlugin, self).get_auth_ref(session, **kwargs)


class VomsV2Loader(loading.BaseV2Loader):
    @property
    def plugin_class(self):
        return VomsV2AuthPlugin

    def get_options(self):
        options = super(VomsV2Loader, self).get_options()

        options.extend([
            loading.Opt('x509-user-proxy',
                        default=None,
                        help=("VOMS proxy to use with 'voms' auth system. "
                              "Defaults to env[OS_X509_USER_PROXY].")),
        ])
        return options
