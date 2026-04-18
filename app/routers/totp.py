from fastapi import APIRouter, Request, HTTPException
from app.limiter import limiter
from pydantic import BaseModel, Field
from argon2 import PasswordHasher
from app.crypto import encrypt
from app.database import generate_client_number, verify_client, insert_client, insert_secret, remove_client, remove_secret

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



    

