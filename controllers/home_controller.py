from flask import Blueprint, render_template
from models.books_model import Book

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    books = Book.query.all()
    return render_template('home.html', books=books)
