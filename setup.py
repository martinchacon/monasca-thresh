# Copyright 2020 FUJITSU LIMITED
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# THIS FILE IS MANAGED BY THE GLOBAL REQUIREMENTS REPO - DO NOT EDIT
import setuptools

# In python < 2.7.4, a lazy loading of package `pbr` will break
# setuptools if some other modules registered functions in `atexit`.
# solution from: http://bugs.python.org/issue15881#msg170215
try:
    import multiprocessing  # noqa
except ImportError:
    pass

setuptools.setup(
    setup_requires=['pbr>=2.0.0'],
    pbr=True)

'''
from setuptools import setup

setup(
    name='monasca-thresh',
    version='1.0.0',
    packages=['monasca_thresh', 'monasca_thresh.conf', 'monasca_thresh.tests', 'monasca_thresh.common',
              'monasca_thresh.common.repositories', 'monasca_thresh.common.repositories.orm',
              'monasca_thresh.common.repositories.base', 'monasca_thresh.common.repositories.sqla',
              'monasca_thresh.common.repositories.mysql'],
    url='https://github.com/openstack/monasca-thresh',
    license='Apache',
    author='OpenStack',
    author_email='openstack-discuss@lists.openstack.org',
    description='Computes thresholds on metrics and publishes alarms to Kafka when exceeded. The current state is also saved in the MySQL database.'
)
'''