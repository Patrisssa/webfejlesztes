from models import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_admin = db.Column(db.Boolean, nullable=False, default=0)

    def __repr__(self):
        return f'<User {self.username}>'

    # Jelszó titkosítása a regisztrációnál
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Jelszó ellenőrzése a bejelentkezésnél
    def check_password(self, password):
        return check_password_hash(self.password, password)

