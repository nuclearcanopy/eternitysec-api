from fastapi.testclient import TestClient
from app.main import app

import re
import pytest

client = TestClient(app)

dummy_pin = "010101"
dummy_label = "grok auth code"
dummy_secret = "I65VU7K5ZQL7WB4E"

@pytest.fixture(scope="session")
def client_number():
    r = client.post(
        "/totp/account",
        json={ "pin": dummy_pin }
    )
    assert r.status_code == 200
    number = r.json()["client_number"]
    assert len(number) == 16
    assert number.isdigit()
    return number


@pytest.fixture(scope="session")
def client_number_with_secret(client_number):
    r = client.post(
        "/totp/secret",
        json={
            "number": client_number,
            "pin": dummy_pin,
            "label": dummy_label,
            "secret": dummy_secret,
        },
    )
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    return client_number

def test_account_number_format(client_number):
    assert len(client_number) == 16

def test_post_secret(client_number_with_secret):
    assert len(client_number_with_secret) == 16

def test_get_code(client_number_with_secret):
    r = client.post(
        "/totp/codes",
        json={
            "number": client_number_with_secret,
            "pin": dummy_pin
        }
    )
    assert r.status_code == 200
    assert r.json()["codes"][0]["label"] == dummy_label


def test_get_codes_schema(client_number_with_secret):
    r = client.post(
        "/totp/codes",
        json={
            "number": client_number_with_secret,
            "pin": dummy_pin
        }
    )
    assert r.status_code == 200

    body = r.json()
    assert "codes" in body
    assert isinstance(body["codes"], list)
    assert len(body["codes"]) >= 1

    first = body["codes"][0]
    assert set(first.keys()) == {"label", "code"}
    assert isinstance(first["label"], str) and first["label"]
    assert isinstance(first["code"], str)
    assert re.fullmatch(r"\d{6}", first["code"])
    
    

    
