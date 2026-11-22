from fastapi.testclient import TestClient
from app.main import app

import random
import subprocess
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

def test_hash(tmp_path):
    r = client.get("/generate-ssh")
    fp = r.json()["sha_fingerprint"]

    # OpenSSH format: "SHA256:" + unpadded base64 of a 32-byte digest = 43 chars -> 50 total
    assert fp.startswith("SHA256:")
    assert "=" not in fp
    assert len(fp) == 50

    # must equal what ssh-keygen reports for the same public key
    pub = tmp_path / "key.pub"
    pub.write_text(r.json()["public_key"] + "\n")
    out = subprocess.run(["ssh-keygen", "-lf", str(pub)], capture_output=True, text=True, check=True).stdout
    assert out.split()[1] == fp
