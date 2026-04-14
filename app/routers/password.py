from fastapi import APIRouter, HTTPException
from app.strength import strength
import random, string

router = APIRouter()

@router.get("/generate-pass")
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

    password = ''.join(random.choices(pool, k = length))
    s = strength(password)
    return {
        "password": password,
        "entropy": s["entropy"],
        "crack_time": s["crack_time"]
    }

@router.get("/calculate-strength")
def calculate_strength(password: str = ''):
    return strength(password)

