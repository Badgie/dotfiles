#!/usr/bin/env python

import json
from urllib import request
from urllib.error import URLError
import subprocess

city = int(subprocess.run(['python', './scrloc.py'], stdout=subprocess.PIPE).stdout.decode('utf-8'))
# 103;overcast, 3;rain, 2;cloudy, 160;light rain, 102;cloudynight, 63;rainshowers, 80;cloudyrain, 180;rainycloudynight


def get_weather_data(url: str) -> str:
    try:
        response = request.urlopen(url, timeout=5).read().decode('utf-8')
    except URLError:
        return "Error getting weather"

    if response is None:
        return "Weather response was null"

    return str(response)


def format_wind_dir(wind: str) -> str:
    if 'V' in wind:
        wind = wind.replace('V', 'W')
    elif 'Ã\u0098' in wind:
        wind = wind.replace('Ã\u0098', 'E')
    return wind


def format_weather_desc(prec: float) -> str:
    if prec < 0.5:
        return 'Drizzle'
    elif prec < 1:
        return 'Light rain'
    elif prec < 2:
        return 'Rain'
    else:
        return 'Heavy rain'


def format_line(data: str) -> str:
    weather = json.loads(data)
    current_hour = weather['timeserie'][0]
    precipitation = float(current_hour['precip1'])
    weather_description = format_weather_desc(precipitation)
    precipitation = f'{round(precipitation, 1)}mm ' if precipitation > 0.0 else ""
    temperature = int(current_hour['temp'])
    humidity = int(current_hour['humidity'])
    wind_direction = format_wind_dir(current_hour['windDir'])
    wind = round(float(current_hour['windSpeed']), 2)

    return f'{weather_description}, {precipitation}{temperature}C {humidity}%RH {wind_direction}{wind}m/s'


if __name__ == '__main__':
    print(format_line(get_weather_data(f'https://www.dmi.dk/NinJo2DmiDk/ninjo2dmidk?cmd=llj&id={city}')))
