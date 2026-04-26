from flask import Blueprint, render_template, redirect, url_for, flash, request
from datetime import datetime, timedelta
from app.models import Transaction, Book, Member

bp = Blueprint('transactions', __name__, url_prefix='/transactions')


@bp.route('/')
def transactions():
    trans_list = Transaction.get_all()
    return render_template('transactions/transactions.html', transactions=trans_list)


@bp.route('/issue', methods=['GET', 'POST'])
def issue_book():
    if request.method == 'POST':
        book_id = request.form['book_id']
        member_id = request.form['member_id']
        due_days = int(request.form['due_days'])
        due_date = (datetime.now() + timedelta(days=due_days)).strftime('%Y-%m-%d')

        Transaction.issue(book_id, member_id, due_date)
        flash('Book issued successfully!', 'success')
        return redirect(url_for('transactions.transactions'))

    books = Book.get_available()
    members = Member.get_active()
    return render_template('transactions/issue_book.html', books=books, members=members)


@bp.route('/return/<int:id>')
def return_book(id):
    trans = Transaction.get_by_id(id)
    if trans:
        Transaction.return_book(id, trans['book_id'])
        flash('Book returned successfully!', 'success')
    return redirect(url_for('transactions.transactions'))
