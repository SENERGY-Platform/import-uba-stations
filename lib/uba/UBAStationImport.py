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

from datetime import date, timezone, datetime, timedelta, time
from typing import List, Tuple, Dict

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
        self.__allow_incomplete_after_hours = timedelta(hours=self.__lib.get_config("AllowIncompleteAfterHours", 96))
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
        earliest: datetime = datetime.combine(since_date, time(hour=1), tzinfo=timezone.utc)
        self.__station_latest: Dict[str, datetime] = {}
        found_latest: Dict[str, bool] = {}
        for station in self.__req_stations:
            self.__station_latest[station.id] = earliest
            found_latest[station.id] = False
        previous_points = self.__lib.get_last_n_messages(
            len(self.__req_stations) * 100)  # need at least one per station
        if previous_points is not None:
            previous_points = previous_points[::-1]  # reverse list, newest msgs have the lowest index now
            for point in previous_points:
                if not found_latest[point[1]["meta"]["station_id"]]:
                    self.__station_latest[point[1]["meta"]["station_id"]] = (point[0].replace(tzinfo=timezone.utc) + timedelta(hours=1))
                    found_latest[point[1]["meta"]["station_id"]] = True

    def import_since_last_run(self):
        now = datetime.now(timezone.utc)
        start = min(self.__station_latest.values())
        next_end = start + slice_size
        count = 0
        count += self.__import_slice(next_end)
        logger.info("Got " + str(count) + " new values")
        while now > next_end:
            start = next_end  # works in python by value
            next_end = start + slice_size
            new_values = self.__import_slice(next_end)
            logger.info("Got " + str(new_values) + " new values")
            count += new_values

    def __import_slice(self, end: datetime) -> int:
        values: List[Tuple[datetime, Value]] = []

        for station in self.__req_stations:
            station_data = self.__fetcher.get_data(station, self.__station_latest[station.id], end, self.__allow_incomplete_after_hours)
            if len(station_data) > 0:
                self.__station_latest[station.id] = (
                            station_data[len(station_data) - 1][0] + timedelta(hours=1)).astimezone(timezone.utc)
            values.extend(station_data)

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
