from fastapi import FastAPI
from app.database import init_db
from app.routers import password, ssh, totp

app = FastAPI()
init_db()

app.include_router(password.router)
app.include_router(ssh.router)
app.include_router(totp.router)
