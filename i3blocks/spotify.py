#!/usr/bin/env python
import subprocess
status = subprocess.run(['playerctl', 'status'], stdout=subprocess.PIPE).stdout.decode('utf-8')

if 'Playing' in status:
    artist = subprocess.run(['playerctl', 'metadata', 'xesam:artist'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', '')
    song = subprocess.run(['playerctl', 'metadata', 'xesam:title'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', '')

    print(f'\u266B {artist} - {song}')
elif 'Paused' in status:
    print(f'\u266B paused')
else:
    print(f'\u266B player not launched')
