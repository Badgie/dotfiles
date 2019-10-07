#!/usr/bin/env python

import subprocess

note = '\u266B'

status = subprocess.run(['playerctl', '--player=spotify', 'status'], stdout=subprocess.PIPE).stdout.decode('utf-8')

if 'Playing' in status:
    artist = subprocess.run(['playerctl', 'metadata', 'xesam:artist'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', '')
    song = subprocess.run(['playerctl', 'metadata', 'xesam:title'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', '')

    print(f'{note} {artist} - {song}')
elif 'Paused' in status:
    print(f'{note} paused')
else:
    print(f'{note} player not launched')
