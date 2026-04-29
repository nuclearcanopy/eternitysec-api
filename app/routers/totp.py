from fastapi import APIRouter, Request, HTTPException
from app.limiter import limiter
from pydantic import BaseModel, Field
from argon2 import PasswordHasher
from app.crypto import encrypt, decrypt
from app.database import generate_client_number, verify_client, insert_client, insert_secret, remove_client, remove_secret, get_secrets
from app.totp_engine import generate_totp
import base64

router = APIRouter()

ph = PasswordHasher()

class ClientRegisterRequest(BaseModel):
    pin: str = Field(min_length=6)

class ClientDeleteRequest(BaseModel):
    number: str = Field(min_length=16)
    pin: str = Field(min_length=6)

class SecretPostRequest(BaseModel):
    number: str = Field(min_length=16)
    pin: str = Field(min_length=6)
    label: str = Field(min_length=1)
    secret: str = Field(min_length=16)

class SecretDeleteRequest(BaseModel):
    number: str = Field(min_length=16)
    pin: str = Field(min_length=6)
    label: str = Field(min_length=1)

class CodesGetRequest(BaseModel):
    number: str = Field(min_length=16)
    pin: str = Field(min_length=6)

@router.post("/totp/account")
@limiter.limit("3/hour")
def register_client(request: Request, body: ClientRegisterRequest):
    pin_hash = ph.hash(body.pin)
    number = generate_client_number()
    insert_client(number, pin_hash)
    return {"client_number": number}

@router.post("/totp/secret")
@limiter.limit("1/sec")
def post_secret(request: Request, body: SecretPostRequest):
    if not verify_client(body.number, body.pin):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        insert_secret(body.number, body.label, encrypt(body.secret.encode()))
        return {"status": "ok"}

@router.delete("/totp/account")
@limiter.limit("1/hour")
def delete_client(request: Request, body: ClientDeleteRequest):
    if not verify_client(body.number, body.pin):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        remove_client(body.number)
        return {"status": "ok"}

@router.delete("/totp/secret")
@limiter.limit("1/sec")
def delete_secret(request: Request, body: SecretDeleteRequest):
    if not verify_client(body.number, body.pin):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        remove_secret(body.number, body.label)
        return {"status": "ok"}    

# tba: get one specific code, not all at once

@router.post("/totp/codes_encrypted")
@limiter.limit("3/minute")
def get_encrypted_codes(request: Request, body: CodesGetRequest):
    if not verify_client(body.number, body.pin):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        return {"secrets": [{"label": label, "encrypted_secret": base64.b64encode(encrypted_secret).decode()} for label, encrypted_secret in get_secrets(body.number)]}

@router.post("/totp/codes")
@limiter.limit("3/minute")
def get_codes(request: Request, body: CodesGetRequest):
    if not verify_client(body.number, body.pin):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        return {"codes": [{"label": label, "code": generate_totp(decrypt(encrypted_secret).decode())} for label, encrypted_secret in get_secrets(body.number)]}
