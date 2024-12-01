from flask import Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from .models.books_model import db, Book
from datetime import datetime

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/admin', methods=['GET', 'POST'])
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
def edit_book(id):
    book = Book.query.get(id)
    if request.method == 'POST':
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.description = request.form.get('description')
        book.published_date = datetime.strptime(request.form.get('published_date'), '%Y-%m-%d')
        db.session.commit()
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('edit_book.html', book=book)


@admin_bp.route('/admin/delete/<int:id>', methods=['GET'])
def delete_book(id):
    book = Book.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for('admin.admin_dashboard'))
