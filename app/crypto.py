from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

key_hex = os.environ.get("TOTP_ENCRYPTION_KEY")
if not key_hex:
    raise RuntimeError("TOTP_ENCRYPTION_KEY environment variable not set")
key = bytes.fromhex(key_hex)

aesgcm = AESGCM(key)

def encrypt(data: bytes) -> bytes:
    nonce = os.urandom(12)
    return nonce+aesgcm.encrypt(nonce, data, None)

def decrypt(data: bytes) -> bytes:
    return aesgcm.decrypt(data[:12], data[12:], None)


