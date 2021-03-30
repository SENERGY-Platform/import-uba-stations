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
from typing import Tuple, List

from lib.uba.meta.UBAComponent import UBAComponent
from lib.uba.meta.UBAStation import UBAStation


class Value(object):
    '''
    Class to store value
    '''

    def __init__(self, measurements: List[Tuple[float, UBAComponent]], station: UBAStation):
        self.measurements = measurements
        self.station = station

    def dict(self) -> dict:
        measurements = {}
        for v in self.measurements:
            measurements[v[1].short_name] = {
                v[1].short_name + "_value": v[0],
                v[1].short_name + "_unit": v[1].unit,
                v[1].short_name + "_measurement_pretty": v[1].pretty_name
            }
        d = {
            "measurements": measurements,
            "meta": {
                "station_id": self.station.id,
                "station_name": self.station.name,
                "lat": self.station.lat,
                "long": self.station.long,
                "city": self.station.city,
                "state": self.station.network_code,
            }
        }

        return d
