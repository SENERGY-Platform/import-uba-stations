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

from datetime import date, timedelta
from typing import Dict, List

import requests

from lib.uba.meta.UBAComponent import UBAComponent
from lib.uba.meta.UBAStation import UBAStation

UBA_BASE_URL = "https://www.umweltbundesamt.de/api"
UBA_METADATA_URL = UBA_BASE_URL + "/air_data/v2/meta/json?use=airquality"


class UBAMetadataManager:
    '''
    Class to store UBA Component metadata
    '''

    def __init__(self, start: date):
        self.__components: Dict[str, UBAComponent] = {}
        self.__stations: Dict[str, UBAStation] = {}
        self.refresh_metadata(start)

    def refresh_metadata(self, start: date):
        if start == date.today():
            start -= timedelta(days=1)
        r = requests.get(
            UBA_METADATA_URL + "&date_from=" + start.isoformat() + "&date_to=" + date.today().isoformat())
        if not r.ok:
            raise RuntimeError("Error contacting UBA Api")
        j = r.json()
        components = j["components"]
        for component_id, component in components.items():
            if len(component) != 5:
                raise RuntimeError("UBA Api delievered unknown component format!")
            self.__components[component_id] = UBAComponent(component_id, component[1], component[2], component[3],
                                                           component[4])

        stations = j["stations"]
        for station_id, station in stations.items():
            if len(station) != 20:
                raise RuntimeError("UBA Api delievered unknown component format!")
            active_to = None
            if station[6] is not None:
                active_to = date.fromisoformat(station[6])
            self.__stations[station_id] = UBAStation(station_id, station[1], station[2], station[3],
                                                     station[4], date.fromisoformat(station[5]), active_to, station[7],
                                                     station[8],
                                                     station[9], station[10], station[11], station[12], station[13],
                                                     station[14], station[15], station[16], station[17], station[18],
                                                     station[19])

    def get_component(self, id: str) -> UBAComponent:
        return self.__components[id]

    def get_all_components(self) -> List[UBAComponent]:
        return list(self.__components.values())

    def get_station(self, id: str) -> UBAStation:
        return self.__stations[id]

    def get_all_stations(self) -> List[UBAStation]:
        return list(self.__stations.values())


if __name__ == "__main__":
    manager = UBAMetadataManager(date.today())
    print("init component manager completed")
