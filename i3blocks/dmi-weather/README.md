# DMI Weather
A script created to gather information about current weather from DMI (Danish Meteorological Institute). The script was originally created to function as a block for [i3blocks](https://github.com/vivien/i3blocks), but can also be used as a standalone.

The script uses geo location based on IP address to determine location to gather weather data from, using [IPInfo](https://ipinfo.io/). Output is a string on the form `descriptor, precipitation(if applicable) temperature humidity wind_direction wind_speed`.

Run the script from terminal
```
[usr@host dmi-weather]$ python weather.py
Cloudy, rain, 1.4mm 12C 95%RH SSW2.58m/s
```
or apply as a block in i3blocks or similar
```
[weather]
command=python /path/to/weather.py
interval=300
```
It is assumed  that this is used as a block in i3blocks, as such paths should be changed if it is used elsewhere.

---
Optionally, you can add an IPInfo token in a config file named `token`. This can help avoid potential ratelimiting.