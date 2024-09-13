from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,                                     unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,  unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_name = db.Column(db.String(100), nullable=False)
    donation_type = db.Column(db.String(10), nullable=False, index=True)  # item name or 'dollar'

    item_description = db.Column(db.String(200), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    amount = db.Column(db.Numeric(10, 2), nullable=True) # if type is dollar

    donation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    distribution_date = db.Column(db.DateTime, nullable=True)
    distribution_status = db.Column(db.Boolean, nullable=False, index=True) #true if distributed

