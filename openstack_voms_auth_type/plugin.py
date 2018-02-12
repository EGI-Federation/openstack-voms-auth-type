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


from shutil import copyfileobj
from tempfile import NamedTemporaryFile

from requests import certs

from keystoneauth1 import loading
from keystoneauth1.identity import v2
from positional import positional


class VomsAuthPlugin(v2.Auth):
    @positional()
    def __init__(self, x509_user_proxy=None, **kwargs):
        # remove v2 auth not valid args
        if 'project_id' in kwargs:
            kwargs['tenant_id'] = kwargs['project_id']
            del kwargs['project_id']
        if 'project_name' in kwargs:
            kwargs['tenant_name'] = kwargs['project_name']
            del kwargs['project_name']
        super(VomsAuthPlugin, self).__init__(**kwargs)
        self.x509_user_proxy = x509_user_proxy

    def get_auth_data(self, headers=None):
        return {'voms': True}

    def get_auth_ref(self, session, **kwargs):
        if not self.x509_user_proxy:
            msg = 'You need to specify a proxy file when using voms auth'
            raise TypeError(msg)
        session.cert = self.x509_user_proxy
        # Create a temporary CA bundle to make proxy verification work
        verify = session.verify
        with NamedTemporaryFile() as bundle:
            src_bundle = verify
            if src_bundle is True:
                src_bundle = certs.where()
            with open(src_bundle, 'r+b') as src:
                copyfileobj(src, bundle)
            with open(self.x509_user_proxy, 'r+b') as proxy:
                bundle.write(proxy.read())
            bundle.flush()
            session.verify = bundle.name
            r = super(VomsAuthPlugin, self).get_auth_ref(session, **kwargs)
        # Restore default settings to avoid failures in subsequent calls
        session.verify = verify
        session.cert = None
        return r


class VomsLoader(loading.BaseV2Loader):
    @property
    def plugin_class(self):
        return VomsAuthPlugin

    def get_options(self):
        options = super(VomsLoader, self).get_options()

        options.extend([
            loading.Opt('x509-user-proxy',
                        default=None,
                        help=("VOMS proxy to use with 'voms' auth system. "
                              "Defaults to env[OS_X509_USER_PROXY].")),
        ])
        return options
