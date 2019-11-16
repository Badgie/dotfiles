#!/usr/bin/env python

import requests
import subprocess
import webbrowser
import argparse
import time
from bottle import route, run, request
from spotipy import oauth2
from pathlib import Path

parser = argparse.ArgumentParser('like currently playing spotify track')
parser.add_argument('-r', action='store_true', help='unlike currently playing spotify track')

port = 8080
client_id = '466a89a53359403b82df7d714030ec5f'
client_secret = '28147de72c3549e98b1e790f3d080b85'
redirect_uri = f'http://localhost:{port}'
scope = 'user-library-modify'
cache = f'{Path.home()}/.spotisaveoauth'
track_url = 'https://api.spotify.com/v1/me/tracks'

sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope, cache_path=cache)


def authorize():
    webbrowser.open(redirect_uri)
    run(host='', port=port)


@route('/')
def index() -> str:
    access_token = ""
    url = request.url
    code = sp_oauth.parse_response_code(url)
    if code:
        token_info = sp_oauth.get_access_token(code)
        access_token = token_info['access_token']

    if access_token:
        return "<span>Successfully retrieved OAuth token. You may close this tab and start using Spotisave.</span>"
    else:
        return f"<a href='{sp_oauth.get_authorize_url()}'>Login to Spotify</a>"


def refresh_token():
    print('OAuth token invalid, refreshing...')
    sp_oauth.refresh_access_token(sp_oauth.get_cached_token()['refresh_token'])


def get_current_song_uri() -> str:
    return subprocess.run(['playerctl', '--player=spotify', 'metadata', 'mpris:trackid'], stdout=subprocess.PIPE)\
        .stdout.decode('utf-8').strip('\n')


def get_token() -> str:
    token_info = sp_oauth.get_cached_token()
    if token_info:
        if (time.time() + 5) > int(sp_oauth.get_cached_token()['expires_at']):
            refresh_token()
        return sp_oauth.get_cached_token()['access_token']
    else:
        authorize()
        exit(1)


def like_track():
    track_id = get_current_song_uri().split(':')[2]
    params = {'ids': track_id}
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {get_token()}'}
    print('Attempting to like track...')
    response = requests.put(url=track_url, params=params, headers=headers)
    if response.status_code == 200:
        print('Successfully liked track!')
    else:
        print(f'Failed to like track, status code: {response.status_code}')
        print(f'Reason: {response.reason}')
        print(response.content.decode('utf-8'))


def unlike_track():
    track_id = get_current_song_uri().split(':')[2]
    params = {'ids': track_id}
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {get_token()}'}
    print('Attempting to unlike track...')
    response = requests.delete(url=track_url, params=params, headers=headers)
    if response.status_code == 200:
        print('Successfully unliked track!')
    else:
        print(f'Failed to unlike track, status code: {response.status_code}')
        print(f'Reason: {response.reason}')
        print(response.content.decode('utf-8'))


def parse_args():
    args = parser.parse_args()
    if args.r:
        unlike_track()
    else:
        like_track()


if __name__ == '__main__':
    parse_args()
