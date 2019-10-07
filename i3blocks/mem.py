#!/usr/bin/env python

import subprocess
import re

mem = 'MEM:'

ps = subprocess.Popen(['free', '--mega'], stdout=subprocess.PIPE)
mem_status = subprocess.run(['grep', 'Mem'], stdin=ps.stdout, stdout=subprocess.PIPE).stdout.decode('utf-8')

mem_list = re.split(r'[^0-9]+', mem_status)

# ['', total, used, free, shared, buff/cache, available, '']
used = f'{round(int(mem_list[2]) / 1000, 1)}G' if int(mem_list[2]) > 1000 else f'{mem_list[2]}M'
available = f'{round(int(mem_list[6]) / 1000, 1)}G' if int(mem_list[6]) > 1000 else f'{mem_list[6]}M'

# if available is formatted in gigs, no worries
if 'G' in available:
    print(f'{mem} {used} ~ {available}')
else:
    print(f'{mem} HEAVY LOAD: {used} ~ {available}')
