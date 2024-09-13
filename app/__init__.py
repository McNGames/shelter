from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)

login = LoginManager(app)
login.login_view = 'login'

from app import routes, models


with app.app_context():
    db.create_all()
    # Adding default user for demo since we're building DB, this is an obvious bad practice
    user = models.User.query.filter_by(username='admin').first()
    if not user:
        u = models.User(username='admin', email='admin@shelter.com')
        u.set_password('admin')
        db.session.add(u)
        db.session.commit()
