from flask import Flask
from models import db
from controllers.home_controller import home_bp
from controllers.admin_controller import admin_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:BendzsoMarshall02.@localhost/project_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(home_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)