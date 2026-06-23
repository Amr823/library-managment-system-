import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(_file_)), "library.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS members (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT    NOT NULL,
            email     TEXT    UNIQUE NOT NULL,
            phone     TEXT,
            joined_at TEXT    DEFAULT (DATE('now'))
        );
        CREATE TABLE IF NOT EXISTS books (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            title         TEXT    NOT NULL,
            author        TEXT    NOT NULL,
            isbn          TEXT    UNIQUE NOT NULL,
            total_copies  INTEGER NOT NULL DEFAULT 1,
            available     INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS borrowings (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id     INTEGER NOT NULL REFERENCES books(id),
            member_id   INTEGER NOT NULL REFERENCES members(id),
            borrow_date TEXT    NOT NULL DEFAULT (DATE('now')),
            return_date TEXT,
            returned    INTEGER NOT NULL DEFAULT 0
        );
    """)
    conn.commit()
    conn.close()
    print("Database initialized successfully.")
