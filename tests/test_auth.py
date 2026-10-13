import uuid
from datetime import datetime, timedelta, timezone

import jwt

from app.util.security import JWT_ALGORITHM, JWT_SECRET, hash_password, verify_password
PASSWORD = "correct-horse-battery"


def fresh_email():
    return f"{uuid.uuid4().hex}@example.com"


def test_password_hash_round_trip():
    stored = hash_password("s3cret-pass")
    assert "s3cret-pass" not in stored
    assert verify_password("s3cret-pass", stored)
    assert not verify_password("wrong-pass", stored)
    assert hash_password("s3cret-pass") != stored  # salted


def test_register_returns_user_without_password(client):
    email = fresh_email()
    r = client.post("/auth/register", json={"email": email, "password": PASSWORD})
    assert r.status_code == 201
    assert r.json()["email"] == email
    assert "password" not in r.text and "password_hash" not in r.json()


def test_duplicate_email_is_409_case_insensitive(client):
    email = fresh_email()
    assert client.post("/auth/register", json={"email": email, "password": PASSWORD}).status_code == 201
    assert client.post("/auth/register", json={"email": email.upper(), "password": PASSWORD}).status_code == 409


def test_register_validates_input(client):
    assert client.post("/auth/register", json={"email": fresh_email(), "password": "short"}).status_code == 422
    assert client.post("/auth/register", json={"email": "not-an-email", "password": PASSWORD}).status_code == 422


def test_login_rejects_bad_credentials(client):
    email = fresh_email()
    client.post("/auth/register", json={"email": email, "password": PASSWORD})
    wrong_password = client.post("/auth/login", json={"email": email, "password": "wrong-password"})
    unknown_user = client.post("/auth/login", json={"email": fresh_email(), "password": PASSWORD})
    assert wrong_password.status_code == unknown_user.status_code == 401
    assert wrong_password.json() == unknown_user.json()


def test_me_needs_a_valid_token(client, signup):
    assert client.get("/users/me", headers=signup()).status_code == 200
    assert client.get("/users/me").status_code == 401
    assert client.get("/users/me", headers={"Authorization": "Bearer garbage"}).status_code == 401


def test_expired_and_forged_tokens_are_rejected(client, signup):
    user_id = client.get("/users/me", headers=signup()).json()["id"]
    past = datetime.now(timezone.utc) - timedelta(hours=2)
    expired = jwt.encode({"sub": str(user_id), "exp": past + timedelta(hours=1)}, JWT_SECRET, algorithm=JWT_ALGORITHM)
    forged = jwt.encode({"sub": str(user_id)}, "not-the-secret-key-but-long-enough-for-hs256", algorithm=JWT_ALGORITHM)
    for token in (expired, forged):
        assert client.get("/users/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401
