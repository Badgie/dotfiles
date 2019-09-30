#!/usr/bin/env python

import subprocess
import re

ps = subprocess.Popen(['free', '--mega'], stdout=subprocess.PIPE)
mem_status = subprocess.run(['grep', 'Mem'], stdin=ps.stdout, stdout=subprocess.PIPE).stdout.decode('utf-8')

mem_list = re.split(r'[^0-9]+', mem_status)

# ['', total, used, free, shared, buff/cache, available, '']
used = round(int(mem_list[2]) / 1000, 1)
if int(mem_list[6]) < 1000:
    print(f'MEM: HEAVY LOAD: {used}G ; {mem_list[6]}M')
else:
    available = round(int(mem_list[6]) / 1000, 1)
    print(f'MEM: {used}G ; {available}G')
