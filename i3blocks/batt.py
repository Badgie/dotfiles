#!/usr/bin/env python

import subprocess
import re

regex = r'\d+\.\d+'

ps = subprocess.Popen(['upower', '-i', '/org/freedesktop/UPower/devices/battery_BAT0'], stdout=subprocess.PIPE)
status = subprocess.run(['grep', 'energy'], stdin=ps.stdout, stdout=subprocess.PIPE).stdout.decode('utf-8')
status_list = re.split('\n', status)

# [energy, energy-empty, energy-full, energy-full-design, energy-rate]
try:
    current = float(re.search(regex, status_list[0]).group(0))
    full = float(re.search(regex, status_list[2]).group(0))
    print(f'BAT: {round(current / full * 100, 2)}%')
except:
    print(f'BAT: \u2620')
