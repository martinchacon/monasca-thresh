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

"""Thresh Module

   The Thresh computes thresholds on metrics and publishes alarms to Kafka when exceeded.
   The current state is also saved in the MySQL database.

   Start the thresh as stand-alone process by running
   'python3 thresh.py worker -l info --config-file <config file>'
"""

from oslo_log import log

from monasca_thresh import config
from monasca_thresh.common.utils import get_db_repo

LOG = log.getLogger(__name__)


def main():
    """Start Monasca Thresh."""

    config.parse_args()


    try:
        LOG.info('''


      /\/\   ___  _ __   __ _ ___  ___ __ _ 
     /    \ / _ \| '_ \ / _` / __|/ __/ _` |
    / /\/\ \ (_) | | | | (_| \__ \ (_| (_| |
    \/    \/\___/|_| |_|\__,_|___/\___\__,_|
        ______  _                   _         
       /__    || |__  _ __ ___  ___| |__      
         / /| |/ '_ \| '__/ _ \/ __| '_ \     
        / / |/ | | | | | |  __/\__ \ | | |    
       / /     |_| |_|_|  \___||___/_| |/    
       \/

        ''')

        db_repo = get_db_repo()
        db_repo

    except Exception:
        LOG.exception('Error! Exiting.')
        # clean_exit(signal.SIGKILL)


if __name__ == "__main__":
    sys.exit(main())
