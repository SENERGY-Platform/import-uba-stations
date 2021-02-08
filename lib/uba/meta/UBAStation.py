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

from datetime import date
from typing import Optional


class UBAStation(object):
    '''
    Class to store UBA station metadata
    '''

    def __init__(self, id: str, code: str, name: str, city: str, synonym: str, active_from: date,
                 active_to: Optional[date],
                 long: float, lat: float, network_id: str, station_setting_id: str, station_type_id: str,
                 network_code: str, network_name: str, setting_name: str, setting_short_name: str, type: str,
                 street: str, street_number: str, zipcode: str):
        self.id = id
        self.code = code
        self.name = name
        self.city = city
        self.synonym = synonym
        self.active_from = active_from
        self.active_to = active_to
        self.long = long
        self.lat = lat
        self.network_id = network_id
        self.station_setting_id = station_setting_id
        self.station_type_id = station_type_id
        self.network_code = network_code
        self.network_name = network_name
        self.setting_name = setting_name
        self.setting_short_name = setting_short_name
        self.type = type
        self.street = street
        self.street_number = street_number
        self.zipcode = zipcode
