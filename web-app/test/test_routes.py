

def test_index(client):
    """Test the root route '/' returns a 200 OK and expected content."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Flask works" in response.data
