#!/usr/bin/env python

import subprocess
import os

# [vol, sink-mute, src-mute]
status = subprocess.run(['pulseaudio-ctl', 'full-status'], stdout=subprocess.PIPE).stdout.decode('utf-8').split(' ')

if 'no' in status[1]:
    print(f' {status[0]}%')
else:
    os.system(f'echo " M"')
    os.system(f'echo ')
    os.system(f'echo "#F4FA58"')
