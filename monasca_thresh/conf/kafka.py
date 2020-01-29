# Copyright 2020 FUJITSU LIMITED
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_config import cfg

_DEFAULT_URL = '192.168.10.6:9092'

kafka_group = cfg.OptGroup('kafka',
                           title='Kafka Options',
                           help='Options under this group allow to configure '
                                'valid connection or Kafka queue.')

kafka_opts = [
    cfg.ListOpt(name='url',
                default=_DEFAULT_URL, required=True,
                help='List of addresses (with ports) pointing '
                     'at Kafka cluster.')
]


def register_opts(conf):
    conf.register_group(kafka_group)
    conf.register_opts(kafka_opts, group=kafka_group)


def list_opts():
    return {
        kafka_group: kafka_opts
    }
