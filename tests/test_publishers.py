def test_publishers_crud(client):
    created = client.post("/publishers", json={"name": "Test Publisher"})
    assert created.status_code == 201
    publisher_id = created.get_json()["id"]

    assert client.get("/publishers").status_code == 200
    assert client.get(f"/publishers/{publisher_id}").status_code == 200
    assert client.put(f"/publishers/{publisher_id}", json={"name": "New Publisher"}).status_code == 200
    assert client.delete(f"/publishers/{publisher_id}").status_code == 200
