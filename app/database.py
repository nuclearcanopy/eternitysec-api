from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import sqlite3
import random
import string

ph = PasswordHasher()

# fundamental db operation
def get_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    return conn, cursor

def init_db():
    conn, cursor = get_db()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients ( 
            client_number TEXT PRIMARY KEY,
            pin_hash TEXT NOT NULL 
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS secrets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_number TEXT NOT NULL,
            label TEXT NOT NULL,
            encrypted_secret BLOB NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# actual stuff
def generate_client_number():
    conn, cursor = get_db()
    while True:
        number = ''.join(random.choices(string.digits, k=16))
        cursor.execute("SELECT client_number FROM clients WHERE client_number = ?", (number,))
        if cursor.fetchone() is None:
            break
    conn.close()
    return number
    

def insert_client(client_number: str, pin_hash: str):
    conn, cursor = get_db()
    cursor.execute("""
        INSERT INTO clients (client_number, pin_hash) VALUES (?, ?)
    """, (client_number, pin_hash))
    conn.commit()
    conn.close()

def insert_secret(client_number: str, label: str, secret: str):
    conn, cursor = get_db()
    cursor.execute("INSERT INTO secrets (client_number, label, encrypted_secret) VALUES (?, ?, ?)", (client_number, label, secret))
    conn.commit()
    conn.close()   

def remove_client(client_number: str):
    conn, cursor = get_db()
    cursor.execute("DELETE FROM clients WHERE client_number = ?", (client_number,))
    cursor.execute("DELETE FROM secrets WHERE client_number = ?", (client_number,))
    conn.commit()
    conn.close()

def remove_secret(client_number: str, label: str):
    conn, cursor = get_db()
    cursor.execute("DELETE FROM secrets WHERE client_number = ? AND label = ?", (client_number, label))
    conn.commit()
    conn.close()


def get_secrets(client_number: str):
    conn, cursor = get_db()
    cursor.execute("SELECT label, encrypted_secret FROM secrets WHERE client_number = ?", (client_number,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def verify_client(client_number: str, pin: str) -> bool:
    conn, cursor = get_db()
    cursor.execute("SELECT pin_hash FROM clients WHERE client_number = ?", (client_number,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return False
    try:
        ph.verify(row[0], pin)
        return True
    except VerifyMismatchError:
        return False




