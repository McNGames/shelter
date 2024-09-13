import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app
from app import db
from app.models import User, Donation

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Donation': Donation}