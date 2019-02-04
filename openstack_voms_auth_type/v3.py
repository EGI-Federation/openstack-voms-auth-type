# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2018 EGI Foundation
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

from keystoneauth1 import access
from keystoneauth1.identity.v3.federation import FederationBaseAuth
from keystoneauth1 import loading

import utils


class VomsV3AuthPlugin(FederationBaseAuth):
    def __init__(self, auth_url, identity_provider, protocol,
                 x509_user_proxy=None, **kwargs):
        super(VomsV3AuthPlugin, self).__init__(auth_url, identity_provider, protocol,
                                                 **kwargs)
        self.x509_user_proxy = x509_user_proxy

    def get_unscoped_auth_ref(self, session, **kwargs):
        with utils.BundleBuilder(session, self.x509_user_proxy) as p:
            auth_response = session.post(self.federated_token_url,
                                         authenticated=False)
        return access.create(auth_response)


class VomsV3Loader(loading.BaseFederationLoader):
    @property
    def plugin_class(self):
        return VomsV3AuthPlugin

    def get_options(self):
        options = super(VomsV3Loader, self).get_options()

        options.extend([
            loading.Opt('x509-user-proxy',
                        help=("VOMS proxy to use with 'voms' auth system. "
                              "Defaults to env[OS_X509_USER_PROXY].")),
        ])
        return options
