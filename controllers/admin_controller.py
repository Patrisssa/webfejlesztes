from flask import abort, Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_login import current_user
from models.books_model import db, Book
from models.users_model import db, User
from datetime import datetime

admin_bp = Blueprint('admin', __name__, template_folder='templates')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin_dashboard():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        description = request.form.get('description')
        published_date = request.form.get('published_date')
        new_book = Book(
            title=title,
            author=author,
            description=description,
            published_date=datetime.strptime(published_date, '%Y-%m-%d')
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('admin.admin_dashboard'))

    books = Book.query.all()
    return render_template('admin.html', books=books)

@admin_bp.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_book(id):
    book = Book.query.get(id)
    if request.method == 'POST':
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.description = request.form.get('description')
        book.published_date = datetime.strptime(request.form.get('published_date'), '%Y-%m-%d')
        db.session.commit()
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('edit.html', book=book)

@admin_bp.route('/admin/delete/<int:id>', methods=['GET'])
@admin_required
def delete_book(id):
    book = Book.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/users', methods=['GET'])
@admin_required
def users_management():
    users = User.query.all()
    return render_template('users.html', users=users)

@admin_bp.route('/admin/delete_user/<int:id>', methods=['GET'])
@admin_required
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin.users_management'))
