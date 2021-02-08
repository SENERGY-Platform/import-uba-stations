# import-uba-stations

Allows you to import air quality measurements from UBA stations.

## Outputs
* value (float): measurement value
* unit (string): value unit
* measurement (string): The air quality parameter that has been measurement (for example PM10)
* measurement_pretty (string): human friendly version of measurement
* meta (struct):
  * station_id (string): id of the station
  * station_name (string): name of the station
  * lat (float): latitude of station
  * long (float): longitude of station
  * city (string): city of station
  * state (string): political state of station location
    

## Configs
You can filter warnings by location by providing city names and/or station ids and/or state abbreviations.
If a station matches at least one filter criteria, it will be imported. If no filters are given, all stations will be selected.

 * FilterCities (list): List of strings that match a city (for example ["Leipzig", "Berlin"]). Default: []
 * FilterStationIds (list): List of strings that match a station id (for example ["1234", "5678"]). Default: []
 * FilterStates (list): List of strings that match a state. Use two letter abbreviations. For example ["SN", "BE"] would import stations in Saxony and Berlin. Default: []

You can choose if you want to import historical data:
  * since (string): Date string in the format YYYY-MM-DD (for example 2020-12-05). Defaults to the current day.

---

This tool uses publicly available data provided by the German Umweltbundesamt. View the original data [on their website](https://www.umweltbundesamt.de/daten/luft/luftdaten/stationen).
