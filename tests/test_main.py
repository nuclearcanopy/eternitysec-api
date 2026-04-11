from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_default():
    r = client.get("/generate")
    assert r.status_code == 200 and len(r.json()["password"]) == 8

def test_long():
    r = client.get("/generate?length=400")
    assert r.status_code == 200 and len(r.json()["password"]) == 400

def test_empty():
    r = client.get("/generate?useUpper=false&useLower=false&useSpecial=false&useDigits=false")
    assert r.status_code == 400
