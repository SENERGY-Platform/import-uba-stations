#  Copyright 2021 InfAI (CC SES)
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

from datetime import date, datetime, timedelta
from datetime import timezone as dttz
from dateutil import tz
from typing import Tuple, List

import requests
from import_lib.import_lib import get_logger
from pytz import timezone

from lib.uba.data.Value import Value
from lib.uba.meta.UBAComponent import UBAComponent
from lib.uba.meta.UBAMetadataManager import UBAMetadataManager
from lib.uba.meta.UBAStation import UBAStation

UBA_BASE_URL = "https://www.umweltbundesamt.de/api"
UBA_DATA_URL = UBA_BASE_URL + "/air_data/v2/airquality/json"
logger = get_logger(__name__)


class UBADataFetcher:
    def __init__(self, metadata: UBAMetadataManager):
        self.__metadata = metadata
        self.__zone = timezone('Europe/Berlin')

    def get_data(self, station: UBAStation, dt_from: datetime, dt_to: datetime, ignore_incomplete_after: timedelta) -> List[Tuple[datetime, Value]]:
        dt_from_local = dt_from.astimezone(tz.gettz('Europe/Berlin'))
        dt_to_local = dt_to.astimezone(tz.gettz('Europe/Berlin'))
        url = UBA_DATA_URL + "?station=" + station.id + "&date_from=" + dt_from_local.date().isoformat() + "&date_to=" + dt_to_local.date().isoformat() + "&time_from=" + str(
            dt_from_local.time().hour) + "&time_to=" + str(dt_to_local.time().hour)
        logger.debug("Fetching: " + url)
        r = requests.get(url)
        if not r.ok:
            raise RuntimeError("Error contacting UBA Api")
        j = r.json()
        time_values: List[Tuple[datetime, Value]] = []
        if "data" not in j or station.id not in j["data"]:
            return time_values
        measurements = j["data"][station.id]
        for _, measurement in measurements.items():
            # measurement[0] can be sth like '2020-12-01 24:00:00'
            if measurement[0].endswith('24:00:00'):
                measurement[0] = measurement[0][:11] + '23:59:59'
            t: datetime = self.__zone.localize(datetime.fromisoformat(measurement[0]))
            incomplete = measurement[2] == 1
            if incomplete and (t + ignore_incomplete_after).astimezone(dttz.utc) < datetime.utcnow().replace(tzinfo=dttz.utc):
                break
            points = measurement[3:]
            values: List[Tuple[float, UBAComponent]] = []
            for point in points:
                values.append((point[1], self.__metadata.get_component(str(point[0]))))
            time_values.append((t, Value(values, station)))
        return time_values


if __name__ == "__main__":
    manager = UBAMetadataManager(date.today())
    fetcher = UBADataFetcher(manager)
    now_sub172h = datetime.now() - timedelta(hours=172)
    values = fetcher.get_data(manager.get_station("215"), now_sub172h, datetime.now(), timedelta(hours=96))
    import json

    for time, value in values:
        print(str(time), json.dumps(value.dict(), ensure_ascii=False))
