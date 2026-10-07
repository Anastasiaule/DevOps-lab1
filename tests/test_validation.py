def test_create_author_with_blank_name_is_rejected(client):
    response = client.post("/authors", json={"name": "   "})

    assert response.status_code == 400


def test_update_author_with_empty_name_is_rejected(client):
    created = client.post("/authors", json={"name": "Tolstoy"})
    assert created.status_code == 201
    author_id = created.get_json()["id"]

    response = client.put(f"/authors/{author_id}", json={"name": ""})

    assert response.status_code == 400


def test_create_author_with_valid_name_still_works(client):
    response = client.post("/authors", json={"name": "Chekhov"})

    assert response.status_code == 201