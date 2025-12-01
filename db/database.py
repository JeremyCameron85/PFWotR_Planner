import sqlite3

DB_FILE = "characters.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            race TEXT,
            class TEXT,
            level INTEGER
        )
    ''')
    conn.commit()
    conn.close()