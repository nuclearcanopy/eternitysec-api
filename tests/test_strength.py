from fastapi.testclient import TestClient
from app.main import app

import urllib.parse

client = TestClient(app)

def test_empty():
    r = client.get("/calculate-strength?password=")
    
    assert r.status_code == 200
    assert r.json()["entropy"] == 0
    assert r.json()["crack_time"] == "less than a second"

def test_strong():
    test = "hm%C!}n7=c,D+1_Q.YY,2TJm^u,nd5#7rH)@egdZfAhN3Z}JXa!Ke}]b]eE~3ym1)8brykN-e*yie2waNAhohqF!TkB~3?AAnJ%5"
    r = client.get("/calculate-strength?password=" + urllib.parse.quote(test) )
    
    assert r.status_code == 200
    assert r.json()["crack_time"] == "longer than the Sun's remaining lifespan"

def test_weak():
    r = client.get("/calculate-strength?password=a")

    assert r.status_code == 200
    assert r.json()["crack_time"] == "less than a second"
