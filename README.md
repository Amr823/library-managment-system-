# Library Management System

A command-line application built with **Python + SQLite** that supports full **CRUD** operations for books, members, and borrowing records.

---

## Features

| Feature | Details |
|---|---|
| Books | Add, list, search, update, delete |
| Members | Register, list, search, update, delete |
| Borrowings | Borrow book, return book, list active/all |
| Database | SQLite (no setup required) |
| Tests | pytest – 10 unit tests |

---

## Project Structure

```
library_management/
├── main.py              # CLI entry point
├── requirements.txt
├── README.md
├── library.db           # Created automatically on first run
├── src/
│   ├── __init__.py
│   ├── database.py      # DB connection & table creation
│   ├── books.py         # Book CRUD operations
│   ├── members.py       # Member CRUD operations
│   └── borrowings.py    # Borrowing & return operations
├── sql/
│   ├── schema.sql       # Table definitions (reference)
│   └── sample_data.sql  # Sample data for manual testing
└── tests/
    └── test_library.py  # 10 unit tests (pytest)
```

---

## Setup & Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/library-management-system.git
cd library-management-system
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python main.py
```

### 4. Run the tests

```bash
python -m pytest tests/ -v
```

---

## Usage – CLI Menu

```
MAIN MENU
1. Books
2. Members
3. Borrowings
0. Exit
```

Each sub-menu lets you perform all CRUD operations interactively.

---

## Database Schema

### members
| Column | Type | Notes |
|---|---|---|
| id | INTEGER | Primary key |
| name | TEXT | Not null |
| email | TEXT | Unique |
| phone | TEXT | Optional |
| joined_at | TEXT | Auto-set to today |

### books
| Column | Type | Notes |
|---|---|---|
| id | INTEGER | Primary key |
| title | TEXT | Not null |
| author | TEXT | Not null |
| isbn | TEXT | Unique |
| total_copies | INTEGER | Default 1 |
| available | INTEGER | Updated on borrow/return |

### borrowings
| Column | Type | Notes |
|---|---|---|
| id | INTEGER | Primary key |
| book_id | INTEGER | FK → books |
| member_id | INTEGER | FK → members |
| borrow_date | TEXT | Auto-set to today |
| return_date | TEXT | Set on return |
| returned | INTEGER | 0 = active, 1 = returned |

---

## Technology Stack

- **Language:** Python 3.8+
- **Database:** SQLite (built-in, no installation needed)
- **Testing:** pytest
- **Version Control:** Git / GitHub

---

## Author

Amriddin – OSTİM Technical University  
Course: IYU 228 – Workplace Application Course
