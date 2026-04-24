from fastapi.testclient import TestClient
from app.main import app

import urllib.parse

client = TestClient(app)

dummy_pin = "010101"
dummy_label = "grok auth code"
dummy_secret = "I65VU7K5ZQL7WB4E"

account_number = 0;

def test_account_number_format():
    r = client.post("/totp/account", json={"pin": dummy_pin})
    assert r.status_code = 200
    account_number = r.json()["account_number"]
    assert len(account_number) = 16

def test_post_secret():
    r = client.post("/totp/secret", json={"number": account_number, "pin": dummy_pin, "label": dummy_label, "secret": dummy_secret})
    assert r.status_code = 200
    assert r.json()["status"] = "ok"

def test_get_code():
    r = client.get("/totp/codes", json={"number": account_number, "pin": dummy_pin})
    assert r.json()["codes"][0]["label"] == "grok auth code"

    
    

    
