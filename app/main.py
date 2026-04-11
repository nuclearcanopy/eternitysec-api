from fastapi import FastAPI, HTTPException
import random
import string

app = FastAPI()

@app.get("/generate")
def generate(length: int = 8, useUpper: bool = True, useLower: bool = True, useSpecial: bool = True, useDigits: bool = True):
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


