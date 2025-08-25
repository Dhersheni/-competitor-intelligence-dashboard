import sqlite3, os
from typing import Optional, Tuple

DB_PATH = "data/db/competitor.db"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS pages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        url TEXT UNIQUE
    );
    CREATE TABLE IF NOT EXISTS snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        page_id INTEGER,
        ts TEXT,
        text_path TEXT,
        html_path TEXT,
        png_path TEXT,
        FOREIGN KEY(page_id) REFERENCES pages(id)
    );
    CREATE TABLE IF NOT EXISTS changes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        page_id INTEGER,
        ts TEXT,
        diff_text TEXT,
        summary TEXT,
        visual_score REAL,
        visual_diff_path TEXT,
        FOREIGN KEY(page_id) REFERENCES pages(id)
    );
    """)
    con.commit()
    con.close()

def get_or_create_page(name: str, url: str) -> int:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT id FROM pages WHERE url = ?", (url,))
    row = cur.fetchone()
    if row:
        pid = row[0]
    else:
        cur.execute("INSERT INTO pages(name,url) VALUES(?,?)", (name,url))
        con.commit()
        pid = cur.lastrowid
    con.close()
    return pid

def last_snapshot_for(page_id: int) -> Optional[Tuple[int, str, str]]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT id, ts, png_path FROM snapshots WHERE page_id = ? ORDER BY id DESC LIMIT 1", (page_id,))
    row = cur.fetchone()
    con.close()
    return row  # (id, ts, png_path) or None

def insert_snapshot(page_id: int, ts: str, text_path: str, html_path: str, png_path: str) -> int:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO snapshots(page_id, ts, text_path, html_path, png_path) VALUES(?,?,?,?,?)",
        (page_id, ts, text_path, html_path, png_path)
    )
    con.commit()
    sid = cur.lastrowid
    con.close()
    return sid

def insert_change(page_id: int, ts: str, diff_text: str, summary: str, visual_score: float, visual_diff_path: str):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO changes(page_id, ts, diff_text, summary, visual_score, visual_diff_path) VALUES(?,?,?,?,?,?)",
        (page_id, ts, diff_text, summary, visual_score, visual_diff_path)
    )
    con.commit()
    con.close()