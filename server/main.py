import os

from flask import Flask, session
from flask_cors import CORS

from routes.youtube import youtubeBP
from routes.spotify import spotifyBP

# App config
app = Flask(__name__)
app.register_blueprint(youtubeBP)
app.register_blueprint(spotifyBP)

app.secret_key = os.urandom(64)
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True  # Only enable this in production with HTTPS

cors = CORS(app, origins='http://localhost:5173', supports_credentials=True)

def start_flask_app():
    app.run(port=8080)

if __name__ == '__main__':
    start_flask_app()