from fastapi.testclient import TestClient
from app.main import app
from app.totp_engine import generate_totp

import random
import time

client = TestClient(app)

dummy_secret = "JBSWY3DPEHPK3PXP"

def test_format():
    assert len(generate_totp(dummy_secret)) == 6
    assert generate_totp(dummy_secret).isdigit()

def test_temporality(monkeypatch):
    first = generate_totp(dummy_secret)
    second = generate_totp(dummy_secret)
    real_time = time.time
    monkeypatch.setattr("app.totp_engine.time.time", lambda: real_time() + 30) # i feel so smart for this (not at all impressive) (i caused stack overflow by patching time time to call itself)
    assert generate_totp(dummy_secret) != first and first == second

def test_predefined(monkeypatch):
    monkeypatch.setattr("app.totp_engine.time.time", lambda: 1234567890)
    assert generate_totp(dummy_secret) == "742275"
