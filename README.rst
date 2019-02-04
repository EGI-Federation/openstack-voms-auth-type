VOMS authentication plugin for Openstack clients
================================================

This is a plugin for OpenStack Clients which provides client support for
VOMS authentication extensions to OpenStack.

Installation
~~~~~~~~~~~~

Install it via pip::

    pip install openstack-voms-auth-type

Or clone the repo and install it::

    git clone https://github.com/enolfc/openstack-voms-auth-type
    cd openstack-voms-auth-type
    python setup.py install

Usage
~~~~~

CLI
---

You have to specify either `v2voms` or `v3voms` in the `--os-auth-type` option
and provide a valid proxy with `--os-x509-user-proxy`.

v2voms::

    openstack --os-auth-type v2voms --os-x509-user-proxy /tmp/x509up_u1000 token issue

v3voms, add also the protocol and identity provider as shown below::

    openstack --os-auth-type v3voms --os-x509-user-proxy /tmp/x509up_u1000 \
              --os-protocol mapped --os-identity-provider egi.eu token issue
