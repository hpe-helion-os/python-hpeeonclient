#!/usr/bin/env python
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


from setuptools import setup
from setuptools import find_packages

setup(
    name='python-eonclient',
    version='1',
    author='HPE Eon',
    author_email='hpecloud@hpe.com',
    url='http://www.hpe.com/',
    packages=find_packages(exclude=["bin"]),
    scripts=['bin/eon',
             'bin/eon-encrypt',
             ],
    include_package_data=True,
    license='LICENSE.txt',
    description='Python bindings for Eon Services',
    long_description=open('README.txt').read(),
    install_requires=[
        'python-keystoneclient >= 0.7.0',
        'PrettyTable >= 0.7, < 0.8',
        'argparse',
        'iso8601>=0.1.9',
        'six>=1.5.2',
        'simplejson',
        'PyYAML'
    ]
)
