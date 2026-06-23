from .database import get_connection


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
from .database import get_connection
from datetime import date


def borrow_book(book_id, member_id):
    conn = get_connection()
    book = conn.execute("SELECT * FROM books WHERE id=?", (book_id,)).fetchone()
    if not book:
        print("Book not found.")
        conn.close()
        return
    if book["available"] <= 0:
        print("No available copies.")
        conn.close()
        return
    member = conn.execute("SELECT * FROM members WHERE id=?", (member_id,)).fetchone()
    if not member:
        print("Member not found.")
        conn.close()
        return
    conn.execute(
        "INSERT INTO borrowings (book_id, member_id, borrow_date) VALUES (?, ?, ?)",
        (book_id, member_id, str(date.today())),
    )
    conn.execute("UPDATE books SET available = available - 1 WHERE id=?", (book_id,))
    conn.commit()
    conn.close()
    print(f"Book '{book['title']}' borrowed by '{member['name']}'.")


def return_book(borrowing_id):
    conn = get_connection()
    rec = conn.execute("SELECT * FROM borrowings WHERE id=?", (borrowing_id,)).fetchone()
    if not rec:
        print("Borrowing record not found.")
        conn.close()
        return
    if rec["returned"]:
        print("Book already returned.")
        conn.close()
        return
    conn.execute(
        "UPDATE borrowings SET returned=1, return_date=? WHERE id=?",
        (str(date.today()), borrowing_id),
    )
    conn.execute("UPDATE books SET available = available + 1 WHERE id=?", (rec["book_id"],))
    conn.commit()
    conn.close()
    print(f"Borrowing id={borrowing_id} returned successfully.")


def list_borrowings(active_only=False):
    conn = get_connection()
    query = """
        SELECT br.id, b.title, m.name AS member,
               br.borrow_date, br.return_date, br.returned
        FROM borrowings br
        JOIN books b ON br.book_id = b.id
        JOIN members m ON br.member_id = m.id
    """
    if active_only:
        query += " WHERE br.returned = 0"
    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(row) for row in rows]
