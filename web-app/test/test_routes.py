"""Unit tests for basic Flask routes."""


def test_index_route_if_logged_out(client):
    """Test index/homepage route when logged out."""
    response = client.get("/")
    assert response.status_code == 302


def test_login_route(client):
    """Test login page route."""
    response = client.get("/login")
    assert response.status_code == 200


def test_register_route(client):
    """Test registration page route."""
    response = client.get("/register")
    assert response.status_code == 200


def test_upload_recording_route(client):
    """Test registration page route."""
    response = client.get("/upload_recording")
    assert response.status_code == 404


def test_movie_page_route(client):
    """Test movie page route."""
    response = client.get("/movie/movie_name")
    assert response.status_code == 302


def test_movies_saved_route(client):
    """Test movies saved route."""
    response = client.get("/movies_saved")
    assert response.status_code == 302


def test_logout_route(client):
    """Test logout route."""
    response = client.get("/logout")
    assert response.status_code == 302
