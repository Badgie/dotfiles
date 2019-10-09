#!/usr/bin/env python

import subprocess
import os

volume = subprocess.run(['pamixer', '--get-volume'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', '')
mute = subprocess.run(['pamixer', '--get-mute'], stdout=subprocess.PIPE).stdout.decode('utf-8')

if 'false' in mute:
    print(f' {volume}%')
elif 'true' in mute:
    os.system(f'echo " M"')
    os.system(f'echo ')
    os.system(f'echo "#F4FA58"')
