#!/usr/bin/env python

from urllib import request
from urllib.error import URLError
import re

file = open('./cities')
cities = file.read().split('\n')
file.close()


def get_loc() -> str:
    try:
        response = request.urlopen('https://geoiptool.com/', timeout=5).read().decode('utf-8')
    except URLError:
        response = "Failed to get response"
    return response


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
    city = re.findall(r'City:.*</div>', data)[0].strip('City: ').strip('</div>')
    return extract_city_id(city)


if __name__ == "__main__":
    print(extract_city(get_loc()))
