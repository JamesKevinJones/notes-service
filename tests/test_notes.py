def test_health(client):
    assert client.get("/health").json() == {"status": "ok", "db": "up"}


def test_full_crud_cycle(client, signup):
    auth = signup()
    r = client.post("/notes", json={"title": "first", "content": "hello"}, headers=auth)
    assert r.status_code == 201
    note = r.json()
    assert note["title"] == "first" and note["id"] > 0

    assert client.get(f"/notes/{note['id']}", headers=auth).json()["content"] == "hello"
    assert [n["id"] for n in client.get("/notes", headers=auth).json()] == [note["id"]]

    r = client.patch(f"/notes/{note['id']}", json={"content": "edited"}, headers=auth)
    assert r.status_code == 200
    assert r.json()["title"] == "first"
    assert r.json()["content"] == "edited"

    assert client.delete(f"/notes/{note['id']}", headers=auth).status_code == 204
    assert client.get(f"/notes/{note['id']}", headers=auth).status_code == 404


def test_missing_note_is_404_everywhere(client, signup):
    auth = signup()
    assert client.get("/notes/999999", headers=auth).status_code == 404
    assert client.patch("/notes/999999", json={"title": "x"}, headers=auth).status_code == 404
    assert client.delete("/notes/999999", headers=auth).status_code == 404


def test_empty_title_rejected(client, signup):
    assert client.post("/notes", json={"title": ""}, headers=signup()).status_code == 422


def test_notes_require_a_token(client):
    assert client.get("/notes").status_code == 401
    assert client.post("/notes", json={"title": "x"}).status_code == 401


def test_users_cannot_touch_each_others_notes(client, signup):
    alice, bob = signup(), signup()
    note_id = client.post("/notes", json={"title": "alice's"}, headers=alice).json()["id"]

    assert client.get("/notes", headers=bob).json() == []
    assert client.get(f"/notes/{note_id}", headers=bob).status_code == 404
    assert client.patch(f"/notes/{note_id}", json={"title": "pwned"}, headers=bob).status_code == 404
    assert client.delete(f"/notes/{note_id}", headers=bob).status_code == 404

    assert client.get(f"/notes/{note_id}", headers=alice).json()["title"] == "alice's"
