from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_main_resource():
    response_auth = client.get("/")
    assert response_auth.status_code == 200


def test_child_resource():
    response_auth = client.get("/items/3")
    assert response_auth.status_code == 200
