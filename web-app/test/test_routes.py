"""Unit tests for Flask routes."""

def test_index_route(test_client):
    """Test the home route returns the correct response."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Flask works" in response.data
