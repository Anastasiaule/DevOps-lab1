def test_genres_crud(client):
    created = client.post("/genres", json={"name": "Fantasy"})
    assert created.status_code == 201
    genre_id = created.get_json()["id"]

    assert len(client.get("/genres").get_json()) == 1
    assert client.get(f"/genres/{genre_id}").status_code == 200
    assert client.put(f"/genres/{genre_id}", json={"name": "Science Fiction"}).status_code == 200
    assert client.delete(f"/genres/{genre_id}").status_code == 200
