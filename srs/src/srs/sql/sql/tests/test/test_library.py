import sys, os, unittest, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(_file_), ".."))
import src.database as db_module
from src.books import add_book, list_books, search_books, update_book, delete_book
from src.members import add_member, list_members, delete_member
from src.borrowings import borrow_book, return_book, list_borrowings

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        db_module.DB_PATH = self.tmp.name
        db_module.initialize_db()
    def tearDown(self):
        if os.path.exists(self.tmp.name):
            os.remove(self.tmp.name)

class TestBooks(BaseTest):
    def test_add_and_list(self):
        add_book("Clean Code", "Robert Martin", "978-01")
        self.assertEqual(len(list_books()), 1)
    def test_search(self):
        add_book("Clean Code", "Robert Martin", "978-01")
        self.assertEqual(len(search_books("Clean")), 1)
    def test_delete(self):
        add_book("Book", "Author", "978-02")
        delete_book(list_books()[0]["id"])
        self.assertEqual(len(list_books()), 0)

class TestBorrowings(BaseTest):
    def test_borrow_and_return(self):
        add_book("Book", "Author", "978-03", total_copies=2)
        add_member("Alice", "alice@example.com")
        borrow_book(list_books()[0]["id"], list_members()[0]["id"])
        self.assertEqual(list_books()[0]["available"], 1)
        return_book(list_borrowings()[0]["id"])
        self.assertEqual(list_books()[0]["available"], 2)

if _name_ == "_main_":
    unittest.main()
