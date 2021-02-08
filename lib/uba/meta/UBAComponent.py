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


class UBAComponent(object):
    '''
    Class to store UBA Component metadata
    '''
    def __init__(self, id: str, short_name: str, pretty_name: str, unit: str, friendly_name: str):
        self.id = id
        self.short_name = short_name
        self.pretty_name = pretty_name
        self.unit = unit
        self.friendly_name = friendly_name

