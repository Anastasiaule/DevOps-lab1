def test_authors_crud(client):
    created = client.post("/authors", json={"name": "Test Author"})
    assert created.status_code == 201
    author_id = created.get_json()["id"]

    assert client.get("/authors").status_code == 200
    assert client.get(f"/authors/{author_id}").status_code == 200

    updated = client.put(f"/authors/{author_id}", json={"name": "Updated Author"})
    assert updated.status_code == 200

    deleted = client.delete(f"/authors/{author_id}")
    assert deleted.status_code == 200
    assert client.get(f"/authors/{author_id}").status_code == 404
