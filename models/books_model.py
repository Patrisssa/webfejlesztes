from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    published_date = db.Column(db.Date)
    isbn = db.Column(db.String(13), unique=True)

    def __repr__(self):
        return f"<Book {self.title}>"