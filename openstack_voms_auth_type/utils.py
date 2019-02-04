''' Basic common utilities for all versions'''

from shutil import copyfileobj
from tempfile import NamedTemporaryFile

from requests import certs


class BundleBuilder:
    def __init__(self, session, proxy):
        self.session = session
        self.verify = session.verify
        self.cert = session.cert
        self.proxy = proxy
        self.bundle = None

    def __enter__(self):
        if not self.proxy:
            msg = 'You need to specify a proxy file when using voms auth'
            raise TypeError(msg)
        self.session.cert = self.proxy
        if self.verify:
            # Create a temporary CA bundle to make proxy verification work
            self.bundle = NamedTemporaryFile()
            src_bundle = self.verify
            if src_bundle is True:
                src_bundle = certs.where()
            with open(src_bundle, 'rb') as src:
                copyfileobj(src, self.bundle)
            with open(self.proxy, 'rb') as proxy_file:
                self.bundle.write(proxy_file.read())
            self.bundle.flush()
            self.session.verify = self.bundle.name

    def __exit__(self, type, value, traceback):
        self.session.verify = self.verify
        self.session.cert = self.cert 
        if self.bundle:
            self.bundle.close()
