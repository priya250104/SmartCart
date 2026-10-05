from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_register_and_login():
    email = f"test.user.{uuid4().hex}@example.com"
    payload = {"full_name": "Test User", "email": email, "password": "secret123", "phone": "123456"}
    register_response = client.post("/api/auth/register", json=payload)
    assert register_response.status_code == 200
    token_response = client.post("/api/auth/login", json={"email": payload["email"], "password": payload["password"]})
    assert token_response.status_code == 200
    assert "access_token" in token_response.json()


def test_products_list():
    response = client.get("/api/products")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
