#!/usr/bin/env python

import subprocess
import urllib.error
from urllib.request import urlopen

wifi='w:'

ps = subprocess.Popen(['ip', 'addr'], stdout=subprocess.PIPE)
wireless_status = subprocess.run(['grep', 'wlp3s0'], stdin=ps.stdout, stdout=subprocess.PIPE).stdout.decode('utf-8')

if 'UP' in wireless_status:
    try:
        # ping ip to check connection
        urlopen(url='http://216.58.192.142', timeout=1)
        print(f'{wifi} up')
    except urllib.error.URLError:
        print(f'{wifi} connecting')
elif 'DOWN' in wireless_status:
    print(f'{wifi} down')
