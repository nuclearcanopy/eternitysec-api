import base64
import hashlib

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/generate-ssh")
def generate_ssh(name: str = Query(default="", max_length=64)):
    private_key = ed25519.Ed25519PrivateKey.generate()

    return {
        "private_key": private_key.private_bytes(
            encoding = serialization.Encoding.PEM,
            format = serialization.PrivateFormat.OpenSSH,
            encryption_algorithm = serialization.NoEncryption()
        ).decode(),
        "public_key": private_key.public_key().public_bytes(
            encoding = serialization.Encoding.OpenSSH,
            format = serialization.PublicFormat.OpenSSH
        ).decode() + (" " + name if name else ""),
        "sha_fingerprint": "SHA256:"+base64.b64encode(hashlib.sha256(private_key.public_key().public_bytes(
            encoding = serialization.Encoding.Raw,
            format = serialization.PublicFormat.Raw,
        )).digest()).decode().rstrip('=')
     }
