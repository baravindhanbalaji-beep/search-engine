import sqlite3
import os
from config import DB_PATH

def init_database():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS pages(
                id INTEGER PRIMARY KEY,
                url TEXT UNIQUE,
                title TEXT,
                status INTEGER,
                depth INTEGER,
                html_file TEXT,
                timestamp TEXT)"""
    )

    conn.commit()
    conn.close()

def save_metadata(
        page_id,url,title,status,depth,html_file,timestamp
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
            INSERT INTO pages(id,url,title,status,depth,html_file,timestamp)
            VALUES(?,?,?,?,?,?,?)
        """,
        (page_id,url,title,status,depth,html_file,timestamp)
    )

    conn.commit()
    conn.close()