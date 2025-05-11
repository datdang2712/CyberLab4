import sqlite3
import os

DB_PATH = "app/data.db"

def get_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
        cursor.execute("CREATE TABLE comments (id INTEGER PRIMARY KEY, content TEXT)")
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'adminpass')")
        conn.commit()
        conn.close()
