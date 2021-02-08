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

from datetime import date, timezone, datetime, timedelta
from typing import List, Tuple

from import_lib.import_lib import get_logger, ImportLib

from lib.uba.data.UBADataFetcher import UBADataFetcher
from lib.uba.data.Value import Value
from lib.uba.meta.UBAMetadataManager import UBAMetadataManager
from lib.uba.meta.UBAStation import UBAStation

logger = get_logger(__name__)
slice_size = timedelta(days=30)


class UBAStationImport:
    def __init__(self, lib: ImportLib):
        self.__lib = lib
        since = self.__lib.get_config("since", "").strip()
        if len(since) < 4:
            since_date = date.today()
            logger.info("No config 'since' provided or invalid")
        else:
            try:
                since_date = date.fromisoformat(since)
            except ValueError:
                logger.info("No config 'since' provided or invalid")
                since_date = date.fromisoformat(since)
        logger.info("Loading metadata... This usually takes a few seconds...")
        self.__metadata = UBAMetadataManager(since_date)
        self.__fetcher = UBADataFetcher(self.__metadata)
        self.__req_stations = self.__filter_stations(self.__metadata.get_all_stations(),
                                                     self.__lib.get_config("FilterCities", []),
                                                     self.__lib.get_config("FilterStationIds", []),
                                                     self.__lib.get_config("FilterStates", []))
        logger.info('Selected ' + str(len(self.__req_stations)) + ' stations')
        self.__filter_measurements = self.__lib.get_config("FilterMeasurements", None)
        self.__last_run: datetime = datetime.combine(since_date, datetime.min.time(), tzinfo=timezone.utc)
        previous_points = self.__lib.get_last_n_messages(len(self.__req_stations))
        if previous_points is not None:
            previous_points = previous_points[::-1]  # reverse list, newest msgs have lowest index
            if len(previous_points) > 0:
                self.__last_run = previous_points[0][0].astimezone(timezone.utc)

    def import_since_last_run(self):
        self.import_since(self.__last_run)

    def import_since(self, start: datetime):
        now = datetime.now(timezone.utc)
        next_end = start + slice_size
        count = 0
        count += self.__import_slice(start, next_end)
        logger.info("Got " + str(count) + " new values")
        while now > next_end:
            start = next_end  # works in python by value
            next_end = start + slice_size
            new_values = self.__import_slice(start, next_end)
            logger.info("Got " + str(new_values) + " new values")
            count += new_values
        if count > 0:
            self.__last_run = now

    def __import_slice(self, start: datetime, end: datetime) -> int:
        values: List[Tuple[datetime, Value]] = []

        for station in self.__req_stations:
            values.extend(self.__fetcher.get_data(station, start, end, self.__filter_measurements))

        values.sort(key=lambda v: v[0])
        for time, value in values:
            self.__lib.put(time.astimezone(timezone.utc), value.dict())
        return len(values)

    @staticmethod
    def __filter_stations(stations: List[UBAStation], allowed_cities: List[str], allowed_ids: List[str],
                          allowed_states: List[str]) -> List[UBAStation]:
        if len(allowed_cities) == 0 and len(allowed_ids) == 0 and len(allowed_states) == 0:
            return stations
        filtered: List[UBAStation] = []
        for station in stations:
            if station.city in allowed_cities or station.id in allowed_ids or station.network_code in allowed_states:
                filtered.append(station)
        return filtered
