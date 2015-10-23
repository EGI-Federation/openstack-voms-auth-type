# coding=utf-8

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


import os
import setuptools


setuptools.setup(
    name="openstack-voms-auth-type",
    version="1.0",
    author="Enol Fernandez",
    author_email="enolfc@ifca.unican.es",
    description="VOMS-based authentication for Openstack",
    long_description=("This is a plugin for OpenStack Clients which provides "
                      "client support for VOMS authentication extensions to "
                      "OpenStack."),
    license="Apache License, Version 2.0",
    url="https://github.com/enolfc/openstack-voms-auth-type",
    download_url="https://github.com/enolfc/openstack-voms-auth-type/archive/master.tar.gz",
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python"
    ],
    entry_points={
        "keystoneclient.auth.plugin": [
            "v2voms = openstack_voms_auth_type.plugin:VomsAuthPlugin"
        ],
    }
)
