from fastapi import FastAPI, HTTPException, Query
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import random
import string

app = FastAPI()

@app.get("/generate-pass")
def generate_pass(length: int = 8, useUpper: bool = True, useLower: bool = True, useSpecial: bool = True, useDigits: bool = True):
    pool = ""
    
    if useUpper:
        pool += string.ascii_uppercase
    if useLower:
        pool += string.ascii_lowercase
    if useSpecial:
        pool += string.punctuation
    if useDigits:
        pool += string.digits

    if pool == "":
        raise HTTPException(400, detail='All options disabled')

    return {"password": ''.join(random.choices(pool, k = length))}

@app.get("/generate-ssh")
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
            ).decode() + (" " + name if name else "")
     }
