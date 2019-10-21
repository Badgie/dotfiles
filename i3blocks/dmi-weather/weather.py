#!/usr/bin/env python

import json
from urllib import request
from urllib.error import URLError
from pathlib import Path

default_path = f'{Path.home()}/.config/i3blocks/dmi-weather/scrloc.py'
dmi_url = 'https://www.dmi.dk/NinJo2DmiDk/ninjo2dmidk?cmd=llj&id='
ip_url = 'https://ipinfo.io/'

# try opening token file, if not found, pass and continue with default url
try:
    token = open(f'{Path.home()}/.config/i3blocks/dmi-weather/token').readline().strip('\n')
    ip_url += f'?token={token}'
except:
    pass

# Try opening on config-path, if not found, try pwd
try:
    file = open(f'{Path.home()}/.config/i3blocks/dmi-weather/cities')
except:
    file = open("./cities")

cities = file.read().split('\n')
file.close()


# get device location json through ipinfo
def get_loc() -> str:
    try:
        response = request.urlopen(ip_url, timeout=5).read().decode('utf-8')
    except URLError:
        response = "Failed to get response"
    return response


# reformat city name if øæå is present and extract city id
def extract_city_id(city: str) -> int:
    for x in cities:
        if city in x:
            return int(x.split(':')[0])
    # øØ
    if '\u00F8' in city or '\u00D8' in city:
        city = city.replace('\u00F8', 'o').replace('\u00D8', 'O')
    # æÆ
    elif '\u00E6' in city or '\u00C6' in city:
        city = city.replace('\u00E6', 'ae').replace('\u00C6', 'AE')
    # åÅ
    elif '\u00E5' in city or '\u00C5' in city:
        city = city.replace('\u00E5', 'aa').replace('\u00C5', 'Aa')
    else:
        print(f'Error: could not find city \'{city}\'')
        exit(1)
    return extract_city_id(city)


def extract_city(data: str) -> int:
    obj = json.loads(data)
    return extract_city_id(obj['city'])


# retrieve weather data from dmi
def get_weather_data(url: str) -> str:
    try:
        response = request.urlopen(url, timeout=5).read().decode('utf-8')
    except URLError:
        return "Error getting weather"

    if response is None:
        return "Weather response was null"

    return str(response)


# reformat wind direction to english notation
def format_wind_dir(wind: str) -> str:
    if 'V' in wind:
        wind = wind.replace('V', 'W')
    elif 'Ã\u0098' in wind:
        wind = wind.replace('Ã\u0098', 'E')
    return wind


# append rain descriptor if applicable, based on precipitation
def format_desc_with_prec(prec: float, desc: str) -> str:
    if 0.5 > prec > 0.0:
        return f'{desc}, drizzle'
    elif 1 > prec > 0.5:
        return f'{desc}, light rain'
    elif 2 > prec > 1:
        return f'{desc}, rain'
    elif prec > 2:
        return f'{desc}, heavy rain'
    return desc


# format weather decriptor based on dmi icon
def format_weather_desc(prec: float, icon: int) -> str:
    if icon is 1:
        return format_desc_with_prec(prec, 'Sunny')
    elif icon is 2 or 102 or 103:
        return format_desc_with_prec(prec, 'Cloudy')
    elif icon is 3:
        return format_desc_with_prec(prec, 'Overcast')
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


# format output line
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
    print(format_line(get_weather_data(f'{dmi_url}{extract_city(get_loc())}')))
