"""Unit tests for main web-app routes."""

def test_login_page_access(client):
    """Test that the login page is accessible."""
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_register_page_access(client):
    """Test that the register page is accessible."""
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Register" in response.data


def test_redirect_from_home(client):
    """Test that unauthenticated users are redirected from /."""
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data
