from fastapi.testclient import TestClient
from app.api.fast_api import app
import pytest
import os


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def auth_headers(client) -> dict[str, str]:
    response = client.post("/auth/login",
                          data={
                              "username": "admin",
                              "password": os.getenv("ADMIN_TEST_PWD")
                          })
    assert response.status_code == 200

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}