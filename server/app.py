import os

from flask import Flask
from flask_cors import CORS

from server.routes.youtube import youtubeBP
from server.routes.spotify import spotifyBP


# App config
def create_app():
    app = Flask(__name__)
    app.register_blueprint(youtubeBP)
    app.register_blueprint(spotifyBP)

    app.secret_key = os.urandom(64)
    app.config["SESSION_COOKIE_NAME"] = "spotify-login-session"

    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = (
        True  # Only enable this in production with HTTPS
    )

    return app


app = create_app()
cors = CORS(app, origins="http://localhost:5173", supports_credentials=True)

if __name__ == "__main__":
    app.run(port=8080)
