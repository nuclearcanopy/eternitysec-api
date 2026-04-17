from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_pswd_empty():
    r = client.get("/generate-pass?useUpper=false&useLower=false&useSpecial=false&useDigits=false")
    assert r.status_code == 400

def test_pswd_default():
    r = client.get("/generate-pass")
    assert r.status_code == 200 and len(r.json()["password"]) == 8

def test_pswd_long():
    r = client.get("/generate-pass?length=400")
    assert r.status_code == 200 and len(r.json()["password"]) == 400

