import pytest
from server.app import create_app
from unittest.mock import patch, MagicMock


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_spotify_oauth():
    with patch("server.routes.spotify.SpotifyOAuth") as mock_oauth_class:
        mock_oauth = MagicMock()
        mock_oauth.get_authorize_url.return_value = "http://mock_auth_url"
        mock_oauth.get_access_token.return_value = {
            "access_token": "mock_access_token",
            "refresh_token": "mock_refresh_token",
            "expires_at": 9999999999,
        }
        mock_oauth.refresh_access_token.return_value = {
            "access_token": "mock_refreshed_token",
            "refresh_token": "mock_refresh_token",
            "expires_at": 9999999999,
        }
        mock_oauth_class.return_value = mock_oauth
        yield mock_oauth


@pytest.fixture
def mock_spotify_client():
    with patch("server.routes.spotify.spotipy.Spotify") as mock_spotify_class:
        mock_sp = MagicMock()
        mock_sp.current_user_playlists.return_value = {
            "items": [{"name": "Test Playlist"}]
        }
        mock_sp.playlist_tracks.return_value = {
            "items": [
                {
                    "track": {
                        "name": "Song 1",
                        "id": "123",
                        "artists": [{"name": "Artist"}],
                        "album": {"name": "Album", "images": []},
                    }
                }
            ]
        }
        mock_spotify_class.return_value = mock_sp
        yield mock_sp


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {
        "SPOTIPY_CLIENT_ID": "mock_client_id",
        "SPOTIPY_CLIENT_SECRET": "mock_client_secret"
    }):
        yield