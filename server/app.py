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


FRONTEND_BASE_URL = os.environ.get("FRONTEND_BASE_URL", "http://localhost:5173/")
app = create_app()
cors = CORS(app, origins=FRONTEND_BASE_URL, supports_credentials=True)

if __name__ == "__main__":
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", 8080))
    app.run(host=host, port=port)


@app.route("/health")
def health_check():
    return "OK", 200


@app.route("/ready")
def ready_check():
    return "OK", 200
