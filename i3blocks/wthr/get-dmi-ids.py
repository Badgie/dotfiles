#!/usr/bin/env python

import json

cities = open('/home/badgy/cities/city.list.json').read()
cityjson = json.loads(cities)
line = ''
for x in cityjson:
    country = x['country']
    name = x['name']
    if country == 'DK' and 'Kommune' not in name and 'Region' not in name:
        id = x['id']
        line += f'{id}: {name}\n'

with open('/home/badgy/dotfiles/i3blocks/cities', 'w') as file:
    file.write(line)
