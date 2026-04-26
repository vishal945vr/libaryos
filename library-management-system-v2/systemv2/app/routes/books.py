from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import Book

bp = Blueprint('books', __name__, url_prefix='/books')


@bp.route('/')
def books():
    book_list = Book.get_all()
    return render_template('books/books.html', books=book_list)


@bp.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        genre = request.form['genre']
        quantity = int(request.form['quantity'])

        if Book.create(title, author, isbn, genre, quantity):
            flash('Book added successfully!', 'success')
        else:
            flash('Book with this ISBN already exists!', 'danger')

        return redirect(url_for('books.books'))

    return render_template('books/add_book.html')


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        genre = request.form['genre']
        quantity = int(request.form['quantity'])

        Book.update(id, title, author, isbn, genre, quantity)
        flash('Book updated successfully!', 'success')
        return redirect(url_for('books.books'))

    book = Book.get_by_id(id)
    return render_template('books/edit_book.html', book=book)


@bp.route('/delete/<int:id>')
def delete_book(id):
    Book.delete(id)
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('books.books'))
