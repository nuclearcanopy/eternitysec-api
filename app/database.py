from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import sqlite3, random, string

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

def verify_client(client_number: str, pin: str) -> bool:
    conn, cursor = get_db()
    cursor.execute("SELECT pin_hash FROM clients WHERE client_number = ?", (client_number,))
    row = cursor.fetchone()

    if row is None:
        return False

    try:
        ph.verify(row[0], pin)
        return True
    except VerifyMismatchError:
        return False

    conn.close()




