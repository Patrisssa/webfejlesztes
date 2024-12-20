from flask import Flask, render_template, url_for, redirect, request, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db
from controllers.home_controller import home_bp
from controllers.admin_controller import admin_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:BendzsoMarshall02.@localhost/project_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

        # Keresd meg a felhasználót az adatbázisban
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)  # Bejelentkezteti a felhasználót
            return redirect(url_for('index'))
        else:
            return 'Hibás bejelentkezési adatok!'

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Ellenőrizd, hogy a felhasználó létezik-e
        if User.query.filter_by(username=username).first():
            return 'Felhasználó már létezik'

        new_user = User(username=username, is_admin=False)
        new_user.set_password(password)  # Jelszó titkosítása
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


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

