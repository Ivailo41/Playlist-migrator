# Test /login route
def test_login(client, mock_spotify_oauth, mock_env):
    response = client.get("/login")
    assert response.status_code == 302
    assert response.headers["Location"] == "http://mock_auth_url"


# Test /callback route
def test_callback(client, mock_spotify_oauth):
    with client.session_transaction() as sess:
        pass  # session starts empty
    response = client.get("/callback?code=mock_code")
    assert response.status_code == 302
    assert response.headers["Location"] == "http://localhost:5173/"
    with client.session_transaction() as sess:
        assert "token_info" in sess
        assert sess["token_info"]["access_token"] == "mock_access_token"


# Test /getUserPlaylists route
def test_get_user_playlists(client, mock_spotify_client):
    with client.session_transaction() as sess:
        sess["token_info"] = {
            "access_token": "mock_access_token",
            "expires_at": 9999999999,
        }
    response = client.get("/getUserPlaylists")
    data = response.get_json()
    assert response.status_code == 200
    assert data["items"][0]["name"] == "Test Playlist"


# Test /getPlaylistTracks route
def test_get_playlist_tracks(client, mock_spotify_client):
    with client.session_transaction() as sess:
        sess["token_info"] = {
            "access_token": "mock_access_token",
            "expires_at": 9999999999,
        }
    response = client.get("/getPlaylistTracks?playlistId=123&totalTracks=1")
    data = response.get_json()
    assert response.status_code == 200
    assert len(data["items"]) == 1
    assert data["items"][0]["track"]["name"] == "Song 1"


# Test logout clears session
def test_logout(client):
    with client.session_transaction() as sess:
        sess["token_info"] = {"access_token": "mock_access_token"}
    response = client.get("/logout")
    assert response.status_code == 302
    with client.session_transaction() as sess:
        assert "token_info" not in sess
