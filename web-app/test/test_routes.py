"""Unit tests for the Flask route handlers."""


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Start Recording" in response.data


def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_register_page(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Create an Account" in response.data


def test_movies_saved_redirect(client):
    response = client.get("/movies_saved")
    assert response.status_code in [302, 200]
