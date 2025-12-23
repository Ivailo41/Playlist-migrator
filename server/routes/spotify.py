import spotipy
import os

from spotipy.oauth2 import SpotifyOAuth
from flask import session, request, redirect, jsonify, Blueprint
import time
from spotipy.cache_handler import FlaskSessionCacheHandler

spotifyBP = Blueprint('spotifyBP',__name__)
cacheHandler = FlaskSessionCacheHandler(session)

SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8080/callback'
SCOPES = ["playlist-read-private", "playlist-modify-private"]

@spotifyBP.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@spotifyBP.route('/callback')
def authorize():
    sp_oauth = create_spotify_oauth()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    print(token_info)
    session["token_info"] = token_info
    return redirect("http://localhost:5173/")

@spotifyBP.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('http://localhost:5173/')

@spotifyBP.route('/getUserPlaylists')
def get_user_playlists():
    if not isAuthorized():
        return jsonify({'error': 'Invalid Spotify token'}), 401
    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))

    playlists = sp.current_user_playlists()
    if playlists is None:
        return jsonify({'error': 'Invalid SPotify token'}), 401
    else:
        return playlists

@spotifyBP.route('/getPlaylistTracks')
def get_playlist_tracks():
    if not isAuthorized():
        return jsonify({'error': 'Invalid Spotify token'}), 401
    
    playlistId = request.args.get('playlistId')
    totalTracks = int(request.args.get('totalTracks'))

    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    response = {'items': []}  # Initialize with an empty list for items

    for i in range(0, totalTracks, 100):
        chunk = sp.playlist_tracks(playlistId, fields='items(track(name, id, artists, album(name, images)))', offset=i, limit=100)
        response['items'].extend(chunk['items'])  # Extend the items list with the new items

    if response is None:
        return jsonify({'error': 'Invalid playlistId'}), 400
    else:
        return jsonify(response)

# Checks to see if token is valid and gets a new token if not
def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid


def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=os.environ['SPOTIPY_CLIENT_ID'],
            client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
            redirect_uri=SPOTIPY_REDIRECT_URI,
            cache_handler=cacheHandler,
            scope=SCOPES)

def isAuthorized():
    session['token_info'], authorized = get_token()
    session.modified = True
    return authorized