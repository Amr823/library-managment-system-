from .database import get_connection


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
        "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?"
