"""
Library Management System – CLI
Usage: python main.py
"""

import sys
import os

# Make sure src package is importable
sys.path.insert(0, os.path.dirname(__file__))

from src.database import initialize_db
from src import (
    add_book, list_books, search_books, update_book, delete_book,
    add_member, list_members, search_members, update_member, delete_member,
    borrow_book, return_book, list_borrowings,
)


def print_table(rows, columns=None):
    if not rows:
        print("  (no records)")
        return
    if columns is None:
        columns = list(rows[0].keys())
    col_widths = {c: max(len(str(c)), max(len(str(r.get(c, ""))) for r in rows)) for c in columns}
    header = " | ".join(str(c).ljust(col_widths[c]) for c in columns)
    print(header)
    print("-" * len(header))
    for row in rows:
        print(" | ".join(str(row.get(c, "")).ljust(col_widths[c]) for c in columns))


def books_menu():
    while True:
        print("\n--- BOOKS ---")
        print("1. List all books")
        print("2. Search books")
        print("3. Add book")
        print("4. Update book")
        print("5. Delete book")
        print("0. Back")
        choice = input("Choice: ").strip()

        if choice == "1":
            print_table(list_books())
        elif choice == "2":
            kw = input("Keyword: ").strip()
            print_table(search_books(kw))
        elif choice == "3":
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            isbn = input("ISBN: ").strip()
            copies = int(input("Total copies [1]: ").strip() or "1")
            add_book(title, author, isbn, copies)
        elif choice == "4":
            bid = int(input("Book ID to update: ").strip())
            title = input("New title (leave blank to keep): ").strip() or None
            author = input("New author (leave blank to keep): ").strip() or None
            isbn = input("New ISBN (leave blank to keep): ").strip() or None
            copies_str = input("New total copies (leave blank to keep): ").strip()
            copies = int(copies_str) if copies_str else None
            update_book(bid, title, author, isbn, copies)
        elif choice == "5":
            bid = int(input("Book ID to delete: ").strip())
            delete_book(bid)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def members_menu():
    while True:
        print("\n--- MEMBERS ---")
        print("1. List all members")
        print("2. Search members")
        print("3. Add member")
        print("4. Update member")
        print("5. Delete member")
        print("0. Back")
        choice = input("Choice: ").strip()

        if choice == "1":
            print_table(list_members())
        elif choice == "2":
            kw = input("Keyword: ").strip()
            print_table(search_members(kw))
        elif choice == "3":
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone (optional): ").strip()
            add_member(name, email, phone)
        elif choice == "4":
            mid = int(input("Member ID to update: ").strip())
            name = input("New name (blank to keep): ").strip() or None
            email = input("New email (blank to keep): ").strip() or None
            phone = input("New phone (blank to keep): ").strip() or None
            update_member(mid, name, email, phone)
        elif choice == "5":
            mid = int(input("Member ID to delete: ").strip())
            delete_member(mid)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def borrowings_menu():
    while True:
        print("\n--- BORROWINGS ---")
        print("1. List all borrowings")
        print("2. List active borrowings")
        print("3. Borrow a book")
        print("4. Return a book")
        print("0. Back")
        choice = input("Choice: ").strip()

        if choice == "1":
            print_table(list_borrowings())
        elif choice == "2":
            print_table(list_borrowings(active_only=True))
        elif choice == "3":
            bid = int(input("Book ID: ").strip())
            mid = int(input("Member ID: ").strip())
            borrow_book(bid, mid)
        elif choice == "4":
            brid = int(input("Borrowing record ID: ").strip())
            return_book(brid)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def main():
    initialize_db()
    print("=" * 40)
    print("  Library Management System")
    print("=" * 40)

    while True:
        print("\nMAIN MENU")
        print("1. Books")
        print("2. Members")
        print("3. Borrowings")
        print("0. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            books_menu()
        elif choice == "2":
            members_menu()
        elif choice == "3":
            borrowings_menu()
        elif choice == "0":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
