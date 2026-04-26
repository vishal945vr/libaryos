import sqlite3

DATABASE = 'library.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE,
            genre TEXT,
            quantity INTEGER DEFAULT 1,
            available INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            address TEXT,
            membership_date DATE DEFAULT CURRENT_DATE,
            status TEXT DEFAULT 'active'
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            member_id INTEGER,
            issue_date DATE,
            return_date DATE,
            due_date DATE,
            status TEXT DEFAULT 'issued',
            FOREIGN KEY (book_id) REFERENCES books(id),
            FOREIGN KEY (member_id) REFERENCES members(id)
        );
    ''')
    conn.commit()
    conn.close()


def create_app():
    from flask import Flask
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    app.secret_key = 'library_secret_key_2024'

    init_db()

    from app.routes import main, books, members, transactions
    app.register_blueprint(main.bp)
    app.register_blueprint(books.bp)
    app.register_blueprint(members.bp)
    app.register_blueprint(transactions.bp)

    return app
