#!/usr/bin/env python

import requests
import subprocess
import webbrowser
import json
from bottle import route, run, request
from spotipy import oauth2
from pathlib import Path

port = 8080
client_id = '466a89a53359403b82df7d714030ec5f'
client_secret = '28147de72c3549e98b1e790f3d080b85'
redirect_uri = f'http://localhost:{port}'
scope = 'playlist-modify-public%20playlist-modify-private'
cache = f'{Path.home()}/.spotisaveoauth'
playlist_id = "your-playlist-id"
playlist_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

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
    sp_oauth.refresh_access_token(sp_oauth.get_cached_token()['refresh_token'])


def get_current_song_uri() -> str:
    return subprocess.run(['playerctl', '--player=spotify', 'metadata', 'mpris:trackid'], stdout=subprocess.PIPE)\
        .stdout.decode('utf-8').strip('\n')


def get_token() -> str:
    token_info = sp_oauth.get_cached_token()
    if token_info:
        return sp_oauth.get_cached_token()['access_token']
    else:
        authorize()
        exit(1)


def check_if_song_exists(uri: str) -> bool:
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': f'Bearer {get_token()}'}
    response = requests.get(url=playlist_url, headers=headers)
    tracks = json.loads(response.content.decode('utf-8'))['items']
    for x in tracks:
        if x['track']['uri'] == uri:
            return True
    return False


def add_song():
    uri = get_current_song_uri()
    if check_if_song_exists(uri):
        print('Track is already present in playlist, exiting.')
        exit(1)
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {get_token()}'}
    params = f'uris={uri}'
    response = requests.post(url=playlist_url, headers=headers, params=params)
    if response.status_code == 201:
        print('Successfully added song to playlist')
    elif response.status_code == 401:
        print('OAuth token invalid, refreshing...')
        refresh_token()
        add_song()
    else:
        print(f'Failed to add song to playlist, status code: {response.status_code}')
        print(response.content.decode('utf-8'))


if __name__ == '__main__':
    add_song()
