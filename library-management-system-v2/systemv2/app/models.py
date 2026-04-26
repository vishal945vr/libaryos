import sqlite3
from app import get_db
from datetime import datetime


class Book:
    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books ORDER BY id DESC')
        books = cursor.fetchall()
        conn.close()
        return books

    @staticmethod
    def get_by_id(id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE id=?', (id,))
        book = cursor.fetchone()
        conn.close()
        return book

    @staticmethod
    def get_available():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE available > 0')
        books = cursor.fetchall()
        conn.close()
        return books

    @staticmethod
    def create(title, author, isbn, genre, quantity):
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO books (title, author, isbn, genre, quantity, available)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, author, isbn, genre, quantity, quantity))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False

    @staticmethod
    def update(id, title, author, isbn, genre, quantity):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE books SET title=?, author=?, isbn=?, genre=?, quantity=? WHERE id=?
        ''', (title, author, isbn, genre, quantity, id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books WHERE id=?', (id,))
        conn.commit()
        conn.close()

    @staticmethod
    def search(search_term):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        results = cursor.fetchall()
        conn.close()
        return results


class Member:
    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM members ORDER BY id DESC')
        members = cursor.fetchall()
        conn.close()
        return members

    @staticmethod
    def get_by_id(id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM members WHERE id=?', (id,))
        member = cursor.fetchone()
        conn.close()
        return member

    @staticmethod
    def get_active():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM members WHERE status = "active"')
        members = cursor.fetchall()
        conn.close()
        return members

    @staticmethod
    def create(name, email, phone, address):
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO members (name, email, phone, address) VALUES (?, ?, ?, ?)
            ''', (name, email, phone, address))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False

    @staticmethod
    def update(id, name, email, phone, address, status):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE members SET name=?, email=?, phone=?, address=?, status=? WHERE id=?
        ''', (name, email, phone, address, status, id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM members WHERE id=?', (id,))
        conn.commit()
        conn.close()


class Transaction:
    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.*, b.title as book_title, m.name as member_name
            FROM transactions t
            JOIN books b ON t.book_id = b.id
            JOIN members m ON t.member_id = m.id
            ORDER BY t.issue_date DESC
        ''')
        transactions = cursor.fetchall()
        conn.close()
        return transactions

    @staticmethod
    def get_by_id(id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transactions WHERE id=?', (id,))
        trans = cursor.fetchone()
        conn.close()
        return trans

    @staticmethod
    def issue(book_id, member_id, due_date):
        conn = get_db()
        cursor = conn.cursor()
        issue_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO transactions (book_id, member_id, issue_date, due_date, status)
            VALUES (?, ?, ?, ?, 'issued')
        ''', (book_id, member_id, issue_date, due_date))
        cursor.execute('UPDATE books SET available = available - 1 WHERE id=?', (book_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def return_book(id, book_id):
        conn = get_db()
        cursor = conn.cursor()
        return_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            UPDATE transactions SET return_date=?, status='returned' WHERE id=?
        ''', (return_date, id))
        cursor.execute('UPDATE books SET available = available + 1 WHERE id=?', (book_id,))
        conn.commit()
        conn.close()


class Stats:
    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) as total FROM books')
        total_books = cursor.fetchone()['total']

        cursor.execute('SELECT COALESCE(SUM(available), 0) as available FROM books')
        available_books = cursor.fetchone()['available']

        cursor.execute('SELECT COUNT(*) as total FROM members')
        total_members = cursor.fetchone()['total']

        cursor.execute('SELECT COUNT(*) as total FROM members WHERE status="active"')
        active_members = cursor.fetchone()['total']

        cursor.execute('SELECT COUNT(*) as total FROM transactions')
        total_transactions = cursor.fetchone()['total']

        cursor.execute('SELECT COUNT(*) as total FROM transactions WHERE status="issued"')
        issued_books = cursor.fetchone()['total']

        cursor.execute('''
            SELECT COUNT(*) as total FROM transactions
            WHERE status='issued' AND due_date < date('now')
        ''')
        overdue_books = cursor.fetchone()['total']

        conn.close()
        return {
            'total_books': total_books,
            'available_books': available_books,
            'total_members': total_members,
            'active_members': active_members,
            'total_transactions': total_transactions,
            'issued_books': issued_books,
            'overdue_books': overdue_books
        }
