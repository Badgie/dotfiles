#!/usr/bin/env python

import subprocess

status = subprocess.run(['playerctl', '--player=spotify', 'status'], stdout=subprocess.PIPE).stdout.decode('utf-8')

if 'Playing' in status:
    artist = subprocess.run(['playerctl', 'metadata', 'xesam:artist'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', '')
    song = subprocess.run(['playerctl', 'metadata', 'xesam:title'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', '')

    print(f'{artist} - {song}')
elif 'Paused' in status:
    print(f'paused')
else:
    print(f'player not launched')
