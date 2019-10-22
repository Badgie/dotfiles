#!/usr/bin/env python

import subprocess
import urllib.error
import os
from urllib.request import urlopen


def print_result(status, color):
    os.system(f'echo " {status}"')
    os.system(f'echo ')
    os.system(f'echo "{color}"')


def get_wifi_status() -> str:
    ps = subprocess.Popen(['ip', 'addr'], stdout=subprocess.PIPE)
    return subprocess.run(['grep', 'wlp3s0'], stdin=ps.stdout, stdout=subprocess.PIPE).stdout.decode('utf-8')


def print_line(status: str):
    if 'UP' in status:
        try:
            # ping ip to check connection
            urlopen(url='http://216.58.192.142', timeout=1)
            print_result(status='up', color='#58FA58')
        except urllib.error.URLError:
            print_result(status='connecting', color='#F4FA58')
    elif 'DOWN' in status:
        print_result(status='down', color='#FA5858')


if __name__ == "__main__":
    print_line(get_wifi_status())
