"""Unit tests for basic Flask routes."""


def test_index_route(client):
    """Test index/homepage route."""
    response = client.get("/")
    assert response.status_code == 200


def test_login_route(client):
    """Test login page route."""
    response = client.get("/login")
    assert response.status_code == 200
