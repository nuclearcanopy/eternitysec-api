import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
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

