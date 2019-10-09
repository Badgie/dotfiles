#!/usr/bin/env python

import subprocess
import re
import os

ps = subprocess.Popen(['free', '--mega'], stdout=subprocess.PIPE)
mem_status = subprocess.run(['grep', 'Mem'], stdin=ps.stdout, stdout=subprocess.PIPE).stdout.decode('utf-8')

mem_list = re.split(r'[^0-9]+', mem_status)

# ['', total, used, free, shared, buff/cache, available, '']
used = f'{round(int(mem_list[2]) / 1000, 1)}G' if int(mem_list[2]) > 1000 else f'{mem_list[2]}M'
available = f'{round(int(mem_list[6]) / 1000, 1)}G' if int(mem_list[6]) > 1000 else f'{mem_list[6]}M'

# if available is formatted in gigs, no worries
if 'G' in available:
    print(f' {used} ~ {available}')
else:
    '''
    format block with red text in case of heavy mem load
    i3blocks reads three script output lines; full text, short text, and color, therefore second line is
    necessary for i3blocks to recognise the color on the third line
    color code needs to be enclosed in double quotes
    '''
    os.system(f'echo " HEAVY LOAD: {used} "~" {available}"')
    os.system(f'echo ')
    os.system(f'echo "#FA5858"')
