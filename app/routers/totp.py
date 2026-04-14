from fastapi import APIRouter, Request
from app.limiter import limiter
from pydantic import BaseModel, Field
from argon2 import PasswordHasher
from app.database import generate_client_number, insert_client
import random, string

router = APIRouter()

ph = PasswordHasher()

class RegisterRequest(BaseModel):
    pin: str = Field(min_length=6)

@router.post("/totp/register")
@limiter.limit("3/hour")
def register(request: Request, body: RegisterRequest):
    pin_hash = ph.hash(body.pin)
    number = generate_client_number()
    insert_client(number, pin_hash)
    return {"client_number": number}

