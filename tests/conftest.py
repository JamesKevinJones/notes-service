import uuid

import pytest
from fastapi.testclient import TestClient

from app.application import app

PASSWORD = "correct-horse-battery"


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def signup(client):
    """Registers a fresh user and returns its Authorization header. Call it twice for two users."""

    def _signup():
        email = f"{uuid.uuid4().hex}@example.com"
        assert client.post("/auth/register", json={"email": email, "password": PASSWORD}).status_code == 201
        token = client.post("/auth/login", json={"email": email, "password": PASSWORD}).json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return _signup
