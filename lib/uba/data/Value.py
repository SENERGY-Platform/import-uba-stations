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

from lib.uba.meta.UBAComponent import UBAComponent
from lib.uba.meta.UBAStation import UBAStation


class Value(object):
    '''
    Class to store value
    '''

    def __init__(self, value: float, component: UBAComponent, station: UBAStation):
        self.value = value
        self.component = component
        self.station = station

    def dict(self) -> dict:
        d = {
            "value": self.value,
            "unit": self.component.unit,
            "measurement": self.component.short_name,
            "measurement_pretty": self.component.pretty_name,
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
