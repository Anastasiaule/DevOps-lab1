def test_books_crud(client):
    author = client.post("/authors", json={"name": "Author"}).get_json()["id"]
    genre = client.post("/genres", json={"name": "Fantasy"}).get_json()["id"]
    publisher = client.post("/publishers", json={"name": "Publisher"}).get_json()["id"]

    payload = {
        "title": "Test Book",
        "author_id": author,
        "genre_id": genre,
        "publisher_id": publisher,
        "year": 2026,
    }

    created = client.post("/books", json=payload)
    assert created.status_code == 201
    book_id = created.get_json()["id"]

    assert client.get("/books").status_code == 200
    assert client.get(f"/books/{book_id}").status_code == 200

    payload["title"] = "Updated Book"
    assert client.put(f"/books/{book_id}", json=payload).status_code == 200

    assert client.delete(f"/books/{book_id}").status_code == 200
    assert client.get(f"/books/{book_id}").status_code == 404
