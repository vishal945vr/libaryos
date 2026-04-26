# 📚 Library Management System

A full-featured web-based Library Management System built with Python Flask and SQLite.

## Features
- 📖 Book Management — Add, edit, delete, search books
- 👥 Member Management — Register and manage library members
- 📋 Transactions — Issue and return books with due date tracking
- 📊 Statistics — Dashboard with library overview
- 🔍 Search — Search books by title, author, or ISBN

## Project Structure
```
library-management-system/
├── run.py                      ← Start the app here
├── requirements.txt
├── library.db                  ← Auto-created on first run
├── app/
│   ├── __init__.py             ← App factory & DB init
│   ├── models.py               ← Book, Member, Transaction, Stats
│   └── routes/
│       ├── main.py             ← Home, Statistics, Search
│       ├── books.py            ← Book CRUD routes
│       ├── members.py          ← Member CRUD routes
│       └── transactions.py     ← Issue & Return routes
├── templates/
│   ├── base.html               ← Shared layout
│   ├── index.html
│   ├── statistics.html
│   ├── search_books.html
│   ├── books/
│   ├── members/
│   └── transactions/
└── static/
    ├── css/style.css
    └── js/main.js
```

## Setup & Run

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Run the app
```bash
python run.py
```

### Step 3 — Open in browser
```
http://localhost:5000
```

The SQLite database (`library.db`) is created automatically on first run.
