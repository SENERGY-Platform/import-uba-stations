# Copyright 2021 InfAI (CC SES)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import time

import schedule
from import_lib.import_lib import ImportLib, get_logger

from lib.uba.UBAStationImport import UBAStationImport

if __name__ == '__main__':
    lib = ImportLib()
    logger = get_logger(__name__)
    uba_station_import = UBAStationImport(lib)

    uba_station_import.import_since_last_run()

    logger.info("Setting schedule to run every hour")
    schedule.every().hour.do(uba_station_import.import_since_last_run)

    while True:
        schedule.run_pending()
        time.sleep(10)
