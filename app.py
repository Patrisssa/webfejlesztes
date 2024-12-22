from functools import wraps
from os import abort
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db
from models.users_model import User
from controllers.home_controller import home_bp
from controllers.admin_controller import admin_bp

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{os.getenv("DB_PASSWORD")}@localhost/project_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = os.getenv('FLASK_SECRET_KEY')
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.register_blueprint(home_bp)
app.register_blueprint(admin_bp)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', logged_in=True, is_admin=current_user.is_admin, user=current_user)
    return render_template('index.html', logged_in=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))

        return 'Hibás felhasználónév vagy jelszó'

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('register.html', errors={'email': 'Ezzel az email címmel már létezik regisztráció!'})

        errors = {}

        if len(last_name.strip()) == 0:
            errors['last_name'] = 'A vezetéknév kitöltése kötelező!'
        if len(first_name.strip()) == 0:
            errors['first_name'] = 'A keresztnév kitöltése kötelező!'
        if len(username.strip()) < 3:
            errors['username'] = 'A felhasználónév legalább 3 karakter hosszú kell legyen!'
        if password != confirm_password:
            errors['confirm_password'] = 'A jelszó és a megerősített jelszó nem egyezik!'

        if errors:
            return render_template('register.html', errors=errors)

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            errors['existing'] = 'Ez a felhasználónév vagy email már létezik!'
            return render_template('register.html', errors=errors)

        new_user = User(
            last_name=last_name,
            first_name=first_name,
            username=username,
            email=email,
            password=password
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html', errors={})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sikeres kijelentkezés!', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
@admin_required
@login_required
def admin():
    if current_user.is_admin:
        return render_template('admin.html')
    else:
        return 'Nincs admin jogosultságod'

@app.route('/admin/users', methods=['GET'])
@admin_required
@login_required
def admin_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

from functools import wraps
from os import abort
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db
from models.users_model import User
from controllers.home_controller import home_bp
from controllers.admin_controller import admin_bp

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{os.getenv("DB_PASSWORD")}@localhost/project_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = os.getenv('FLASK_SECRET_KEY')
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.register_blueprint(home_bp)
app.register_blueprint(admin_bp)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', logged_in=True, is_admin=current_user.is_admin, user=current_user)
    return render_template('index.html', logged_in=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))

        return 'Hibás felhasználónév vagy jelszó'

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('register.html', errors={'email': 'Ezzel az email címmel már létezik regisztráció!'})

        errors = {}

        if len(last_name.strip()) == 0:
            errors['last_name'] = 'A vezetéknév kitöltése kötelező!'
        if len(first_name.strip()) == 0:
            errors['first_name'] = 'A keresztnév kitöltése kötelező!'
        if len(username.strip()) < 3:
            errors['username'] = 'A felhasználónév legalább 3 karakter hosszú kell legyen!'
        if password != confirm_password:
            errors['confirm_password'] = 'A jelszó és a megerősített jelszó nem egyezik!'

        if errors:
            return render_template('register.html', errors=errors)

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            errors['existing'] = 'Ez a felhasználónév vagy email már létezik!'
            return render_template('register.html', errors=errors)

        new_user = User(
            last_name=last_name,
            first_name=first_name,
            username=username,
            email=email,
            password=password
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html', errors={})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sikeres kijelentkezés!', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
@admin_required
@login_required
def admin():
    if current_user.is_admin:
        return render_template('admin.html')
    else:
        return 'Nincs admin jogosultságod'

@app.route('/admin/users', methods=['GET'])
@admin_required
@login_required
def admin_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/toggle_admin/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def toggle_admin(id):
    user = User.query.get(id)
    if not user:
        flash('Felhasználó nem található!', 'error')
        return redirect(url_for('admin_users'))

    if user.is_protected == 1:
        flash('Ez a felhasználó védett, az admin státusza nem módosítható!', 'error')
        return redirect(url_for('admin_users'))

    if user.id == current_user.id:
        flash('Nem veheted el a saját admin státuszodat!', 'error')
        return redirect(url_for('admin_users'))

    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f"Az admin jog {user.username} számára módosítva lett!", 'success')
    return redirect(url_for('admin_users'))


@app.route('/profile')
@login_required
def profile():
    user = current_user
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
