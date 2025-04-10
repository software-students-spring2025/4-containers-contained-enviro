def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Flask works" in response.data
