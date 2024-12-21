from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from models import db
from models.users_model import User
from controllers.home_controller import home_bp
from controllers.admin_controller import admin_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:BendzsoMarshall02.@localhost/project_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'your_secret_key'  # Titkos kulcs a session kezeléshez
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.register_blueprint(home_bp)
app.register_blueprint(admin_bp)

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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):  # Jelszó ellenőrzése
            login_user(user)  # Bejelentkezés
            return redirect(url_for('index'))  # Átirányítás a felhasználói dashboardra

        return 'Hibás felhasználónév vagy jelszó'

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
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

        # Hibák ellenőrzése
        errors = {}

        if len(last_name.strip()) == 0:
            errors['last_name'] = 'A vezetéknév kitöltése kötelező!'
        if len(first_name.strip()) == 0:
            errors['first_name'] = 'A keresztnév kitöltése kötelező!'
        if len(username.strip()) < 3:
            errors['username'] = 'A felhasználónév legalább 3 karakter hosszú kell legyen!'
        if password != confirm_password:
            errors['confirm_password'] = 'A jelszó és a megerősített jelszó nem egyezik!'

        # Ha van hiba, visszaadjuk a hibákat
        if errors:
            return render_template('register.html', errors=errors)

        # Ellenőrizzük, hogy van-e már ilyen felhasználónév vagy email
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            errors['existing'] = 'Ez a felhasználónév vagy email már létezik!'
            return render_template('register.html', errors=errors)

        # Új felhasználó létrehozása
        new_user = User(
            last_name=last_name,
            first_name=first_name,
            username=username,
            email=email,
            password=password
        )
        new_user.set_password(password)

        # Felhasználó mentése az adatbázisba
        db.session.add(new_user)
        db.session.commit()

        # Átirányítás a bejelentkezési oldalra
        return redirect(url_for('login'))

    # GET kérés esetén a regisztrációs űrlap visszaadása
    return render_template('register.html', errors={})


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin():
    if current_user.is_admin:
        return render_template('admin_dashboard.html')
    else:
        return 'Nincs admin jogosultságod'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)

