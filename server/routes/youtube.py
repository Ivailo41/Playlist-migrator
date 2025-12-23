from flask import session, request, redirect, jsonify, Blueprint

import os

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

youtubeBP = Blueprint('youtubeBP',__name__)
YTSCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

@youtubeBP.route('/api/youtube/login')
def loginYT():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Get credentials and create an API client
    flow = createYoutubeFlow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    
    session['state'] = state
    print(authorization_url)
    return redirect(authorization_url)

@youtubeBP.route('/api/youtube/callback')
def callback():
    flow = createYoutubeFlow()
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return redirect('http://localhost:5173/')

@youtubeBP.route('/api/youtube/getPlaylists')
def getPlaylistsYT():
    if not isAuthorizedYT():
        return jsonify({'error': 'Invalid Youtube token'}), 401
    
    credentials = createYoutubeCredentials()
    youtube = build('youtube', 'v3', credentials=credentials)
    print(youtube)
    request = youtube.playlists().list(
        part='snippet',
        mine=True
    )
    response = request.execute()
    return jsonify(response)

def createYoutubeFlow():
    client_secrets_file = "server/auth.json"

    flow = Flow.from_client_secrets_file(
        client_secrets_file, scopes=YTSCOPES)
    flow.redirect_uri = 'http://127.0.0.1:8080/api/youtube/callback'
    return flow

def createYoutubeCredentials():
    credentials = Credentials(
    token=session['credentials']['token'],
    refresh_token=session['credentials']['refresh_token'],
    token_uri=session['credentials']['token_uri'],
    client_id=session['credentials']['client_id'],
    client_secret=session['credentials']['client_secret'],
    scopes=session['credentials']['scopes']
)
    return credentials

def isAuthorizedYT():
    return session.get('credentials', False)