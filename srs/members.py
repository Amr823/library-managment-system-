[22:58, 23.06.2026] -: import sqlite3
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
[23:07, 23.06.2026] -: from .database import get_connection


def add_book(title, author, isbn, total_copies=1):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO books (title, author, isbn, total_copies, available) VALUES (?, ?, ?, ?, ?)",
            (title, author, isbn, total_copies, total_copies),
        )
        conn.commit()
        print(f"Book '{title}' added successfully.")
    except Exception as e:
        print(f"Error adding book: {e}")
    finally:
        conn.close()


def list_books():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def search_books(keyword):
    conn = get_connection()
    like = f"%{keyword}%"
    rows = conn.execute(
        "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
[23:08, 23.06.2026] -: from .database import get_connection


def add_member(name, email, phone=""):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO members (name, email, phone) VALUES (?, ?, ?)",
            (name, email, phone),
        )
        conn.commit()
        print(f"Member '{name}' registered.")
    except Exception as e:
        print(f"Error adding member: {e}")
    finally:
        conn.close()


def list_members():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM members").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def search_members(keyword):
    conn = get_connection()
    like = f"%{keyword}%"
    rows = conn.execute(
        "SELECT * FROM members WHERE name LIKE ? OR email LIKE ?", (like, like)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_member(member_id, name=None, email=None, phone=None):
    conn = get_connection()
    m = conn.execute("SELECT * FROM members WHERE id=?", (member_id,)).fetchone()
    if not m:
        print(f"Member id={member_id} not found.")
        conn.close()
        return
    conn.execute(
        "UPDATE members SET name=?, email=?, phone=? WHERE id=?",
        (name or m["name"], email or m["email"],
         phone if phone is not None else m["phone"], member_id),
    )
    conn.commit()
    conn.close()
    print(f"Member id={member_id} updated.")


def delete_member(member_id):
    conn = get_connection()
    active = conn.execute(
        "SELECT COUNT(*) FROM borrowings WHERE member_id=? AND returned=0", (member_id,)
    ).fetchone()[0]
    if active > 0:
        print("Cannot delete: member has active borrowings.")
        conn.close()
        return
    conn.execute("DELETE FROM members WHERE id=?", (member_id,))
    conn.commit()
    conn.close()
    print(f"Member id={member_id} deleted.")
