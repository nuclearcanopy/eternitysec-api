from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_format():
    r = client.get("/generate-ssh?name=Ab01-_")
    assert r.status_code == 200
    assert r.json()["public_key"][:12] == "ssh-ed25519 "
    assert r.json()["public_key"][-7:] == " Ab01-_"

