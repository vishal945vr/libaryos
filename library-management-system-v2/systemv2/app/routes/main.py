from flask import Blueprint, render_template, request
from app.models import Stats, Book

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/statistics')
def statistics():
    stats = Stats.get_all()
    return render_template('statistics.html', **stats)


@bp.route('/search_books', methods=['GET', 'POST'])
def search_books():
    books = []
    search = ''
    if request.method == 'POST':
        search = request.form['search']
        books = Book.search(search)
    return render_template('search_books.html', books=books, search=search)
