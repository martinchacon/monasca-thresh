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

_DEFAULT_DB_HOST = '127.0.0.1'
_DEFAULT_DB_USER = 'root'
_DEFAULT_DB_PASSWORD = 'secretdatabase'  # nosec bandit B105
_DEFAULT_DB_NAME = 'mon'
_DEFAULT_MYSQL_PORT = 3306

db_group = cfg.OptGroup('database',
                        title='Database Options',
                        help='Driver configuration for database connectivity.')

db_opts = [
    cfg.RepoDriverOpt(name='repo_driver',
                      default='monasca_thresh.common.repositories.mysql.mysql_repo:MysqlRepo')
]

mysql_group = cfg.OptGroup('mysql',
                           title='MySQL Options',
                           help='Configuration options to configure '
                                'plain MySQL RBD driver.')

mysql_opts = [
    cfg.HostAddressOpt(name='host', default=_DEFAULT_DB_HOST,
                       help='IP address of MySQL instance.'),
    cfg.PortOpt(name='port', default=_DEFAULT_MYSQL_PORT,
                help='Port number of MySQL instance.'),
    cfg.StrOpt(name='user', default=_DEFAULT_DB_USER,
               help='Username to connect to MySQL '
                    'instance and given database.'),
    cfg.StrOpt(name='passwd', default=_DEFAULT_DB_PASSWORD,
               ignore_case=True, secret=True,
               help='Password to connect to MySQL instance '
                    'and given database.'),
    cfg.DictOpt(name='ssl', default={},
                help='A dict of arguments similar '
                     'to mysql_ssl_set parameters.'),
    cfg.StrOpt(name='db', default=_DEFAULT_DB_NAME,
               help='Database name available in given MySQL instance.')
]


def register_opts(conf):
    conf.register_group(db_group)
    conf.register_group(mysql_group)

    conf.register_opts(db_opts, group=db_group)
    conf.register_opts(mysql_opts, group=mysql_group)


def list_opts():
    return {
        db_group: db_opts,
        mysql_group: mysql_opts,
    }
