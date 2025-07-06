from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_and_login():
    response = client.post("/register", json={"username":"testuser", "password":"testpass"})
    assert response.status_code == 200

    response = client.post("/login", json={"username":"testuser", "password":"testpass"})
    assert "access_token" in response.json()
