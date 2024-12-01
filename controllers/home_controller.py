from flask import Blueprint, render_template
from models.books_model import Book

# Home Blueprint
home_bp = Blueprint('home', __name__)

# Főoldal route
@home_bp.route('/')
def index():
    books = Book.query.all()  # Minden könyv lekérése
    return render_template('home.html', books=books)
