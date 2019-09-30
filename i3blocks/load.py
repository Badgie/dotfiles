#!/usr/bin/env python

load_file = open('/proc/loadavg')
load_list = load_file.read().strip('\n').split(' ')
load_file.close()

# [1 min, 5 min, 10 min]
print(f'LOAD: {load_list[0]}')
