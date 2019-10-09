#!/usr/bin/env python

import subprocess
import re

ps = subprocess.Popen(['sensors'], stdout=subprocess.PIPE)
status_list = subprocess.run(['grep', 'Core'], stdin=ps.stdout, stdout=subprocess.PIPE)\
                .stdout.decode('utf-8').splitlines()

core_temps = ''

for x in status_list:
    core_temps += re.search(r'\d+.\d+', x).group(0).replace('.0', '') + '\u00B0 ~ '

core_temps = core_temps.strip(' ~ ')

print(f' {core_temps}')
