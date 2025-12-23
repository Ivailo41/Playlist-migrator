def test_spotify_get_user_playlists_unauthorized(client):
    response = client.get('/getUserPlaylists')
    assert response.status_code == 401

def test_spotify_login_redirect(client):
    """Test that /login redirects to Spotify auth"""
    response = client.get("/login")
    assert response.status_code == 302
    assert "accounts.spotify.com" in response.headers["Location"]