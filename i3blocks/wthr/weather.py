#!/usr/bin/env python

import json
from urllib import request
from urllib.error import URLError
import subprocess

city = int(subprocess.run(['python', './scrloc.py'], stdout=subprocess.PIPE).stdout.decode('utf-8'))


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


def format_weather_desc(prec: float, icon: int) -> str:
    if icon is 1:
        return 'Sunny'
    elif icon is 2 or 102 or 103:
        return 'Cloudy'
    elif icon is 3:
        return 'Overcast'
    elif icon is 60 or 80 or 160 or 180:
        if prec < 0.5:
            return 'Drizzle'
        else:
            return 'Light rain'
    elif icon is 63 or 81 or 163 or 181:
        if prec < 2:
            return 'Rain'
        else:
            return 'Heavy rain'
    elif icon is 68 or 83 or 168 or 183:
        return 'Light sleet'
    elif icon is 69 or 84 or 169 or 184:
        return 'Sleet'
    elif icon is 70 or 85 or 170 or 185:
        return 'Light snow'
    elif icon is 73 or 86 or 173 or 186:
        return 'Snow'
    elif icon is 95 or 195:
        if prec < 0.5:
            return 'Thunder and drizzle'
        elif prec < 1:
            return 'Thunder and light rain'
        elif prec < 2:
            return 'Thunder and rain'
        else:
            return 'Thunder and heavy rain'
    elif icon is 101:
        return 'Clear sky'



def format_line(data: str) -> str:
    weather = json.loads(data)
    current_hour = weather['timeserie'][0]
    precipitation = round(float(current_hour['precip1']), 1)
    weather_description = format_weather_desc(precipitation, int(current_hour['symbol']))
    precipitation = f'{precipitation}mm ' if precipitation > 0.0 else ""
    temperature = int(current_hour['temp'])
    humidity = int(current_hour['humidity'])
    wind_direction = format_wind_dir(current_hour['windDir'])
    wind = round(float(current_hour['windSpeed']), 2)

    return f'{weather_description}, {precipitation}{temperature}C {humidity}%RH {wind_direction}{wind}m/s'


if __name__ == '__main__':
    print(format_line(get_weather_data(f'https://www.dmi.dk/NinJo2DmiDk/ninjo2dmidk?cmd=llj&id={city}')))
