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

You have to specify the `v2voms` in the `--os-auth-type` option and provide a
valid proxy with `--os-x509-user-proxy`::

    openstack --os-auth-type v2voms --os-x509-user-proxy /tmp/x509up_u1000 token issue

API
---

To be documented
