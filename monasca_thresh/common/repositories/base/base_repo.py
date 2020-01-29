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


class BaseRepo(object):
    def __init__(self, config):

        self._find_all_alarm_definitions_sql = \
            """SELECT id, tenant
               FROM alarm_definition
               WHERE deleted_at is NULL
               ORDER BY created_at"""

        self.find_all_sub_alarm_definition = \
            """SELECT sad.id, sad.metric_name, sadd.dimension_name, sadd.value
               FROM sub_alarm_definition sad
               LEFT OUTER JOIN sub_alarm_definition_dimension sadd
               ON sadd.sub_alarm_definition_id=sad.id
               WHERE sad.alarm_definition_id = %s
               ORDER BY sad.id 
            """
