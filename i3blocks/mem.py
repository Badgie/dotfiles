#!/usr/bin/env python

import subprocess
import re
import os


def get_mem_status() -> list:
    ps = subprocess.Popen(['free', '--mega'], stdout=subprocess.PIPE)
    mem_status = subprocess.run(['grep', 'Mem'], stdin=ps.stdout, stdout=subprocess.PIPE).stdout.decode('utf-8')
    return re.split(r'[^0-9]+', mem_status)


def print_line(status: list):
    # ['', total, used, free, shared, buff/cache, available, '']
    used = f'{round(int(status[2]) / 1000, 1)}G' if int(status[2]) > 1000 else f'{status[2]}M'
    available = f'{round(int(status[6]) / 1000, 1)}G' if int(status[6]) > 1000 else f'{status[6]}M'
    cached = f'{round(int(status[5]) / 1000, 1)}G' if int(status[5]) > 1000 else f'{status[5]}M'

    # if available is formatted in gigs, no worries
    if 'G' in available:
        print(f' {used} ~ {available} (C: {cached})')
    else:
        '''
        format block with red text in case of heavy mem load
        i3blocks reads three script output lines; full text, short text, and color, therefore second line is
        necessary for i3blocks to recognise the color on the third line
        color code needs to be enclosed in double quotes
        '''
        os.system(f'echo " HEAVY LOAD: {used} "~" {available} (C: {cached})"')
        os.system(f'echo ')
        os.system(f'echo "#FA5858"')


if __name__ == "__main__":
    print_line(get_mem_status())
