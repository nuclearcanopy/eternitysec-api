from fastapi.testclient import TestClient
from app.main import app

import random
import string

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import load_ssh_private_key, load_ssh_public_key
from cryptography.exceptions import InvalidSignature


client = TestClient(app)

def test_format():
    r = client.get("/generate-ssh?name=Ab01-_")
    
    public_key = r.json()["public_key"]
    private_key = r.json()["private_key"]

    assert r.status_code == 200
    
    # formatting
    assert public_key.startswith("ssh-ed25519 ")
    assert public_key.strip().endswith(" Ab01-_")

    assert private_key.startswith("-----BEGIN OPENSSH PRIVATE KEY-----")
    assert private_key.strip().endswith("-----END OPENSSH PRIVATE KEY-----")

def test_round_trip():
    r = client.get("/generate-ssh")

    public_key = r.json()["public_key"]
    private_key = r.json()["private_key"]

    # round trip
    priv = load_ssh_private_key(private_key.encode(), password=None)
    pub = load_ssh_public_key(public_key.encode())

    data = ''.join( random.choices(string.ascii_uppercase + string.ascii_lowercase + string.punctuation + string.digits, k=128) )

    signature = priv.sign(data.encode())

    try:
        pub.verify(signature, data.encode())
    except InvalidSignature:
        assert False, "ssh signature verification fail"

def test_hash():
    # would be dumb to check the hash by rehashing as i would be testing hashlib against itself
    r = client.get("/generate-ssh")

    assert r.json()["sha_fingerprint"].startswith("SHA256:")
    assert len(r.json()["sha_fingerprint"]) == 51
