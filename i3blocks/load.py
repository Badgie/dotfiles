#!/usr/bin/env python
import os


def print_result(load, color):
    os.system(f'echo " {load}"')
    os.system(f'echo ')
    os.system(f'echo "{color}"')


load_file = open('/proc/loadavg')
load_list = load_file.read().strip('\n').split(' ')
load_file.close()

# [1 min, 5 min, 10 min]
if float(load_list[0]) > 2.5:
    if float(load_list[0]) > 5.0:
        print_result(load=load_list[0], color='#FA5858')
    else:
        print_result(load=load_list[0], color='#F4FA58')
else:
    print(f' {load_list[0]}')
