#!/usr/bin/env python

import requests
import subprocess
import configparser
from pathlib import Path

config = configparser.ConfigParser()
config.read(f'{Path.home()}/.config/i3/spotisave/config')
token = config['spotify']['token']
headers = {'Content-Type': 'application/json',
           'Authorization': f'Bearer {token}'}
playlist_id = config['spotify']['playlist']


def get_current_song_uri() -> str:
    return subprocess.run(['playerctl', '--player=spotify', 'metadata', 'mpris:trackid'], stdout=subprocess.PIPE)\
        .stdout.decode('utf-8').strip('\n')


def add_song():
    params = f'uris={get_current_song_uri()}'
    response = requests.post(f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', headers=headers,
                             params=params)
    if response.status_code == 201:
        print('Successfully added song to playlist')
    else:
        print(f'Failed to add song to playlist, status code: {response.status_code}')
        print(response.content.decode('utf-8'))


if __name__ == '__main__':
    add_song()
