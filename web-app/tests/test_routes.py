def test_index_route(test_client):
    """Test the index route."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Movie Recommendations For You" in response.data
