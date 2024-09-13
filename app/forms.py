from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.choices import RadioField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import IntegerField, DecimalField
from wtforms.validators import DataRequired, NumberRange, Optional
from datetime import date


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ItemDonationForm(FlaskForm):
    donation_type = StringField('Item Name', validators=[DataRequired()])
    description = StringField('Description')
    quantity = IntegerField('Quantity', validators=[NumberRange(min=1, message="Quantity must be greater than 0")])
    donor_name = StringField('Donor Name', validators=[DataRequired()])
    donation_date = DateField('Date of Donation', format='%Y-%m-%d', default=date.today, validators=[Optional()])

class FinancialDonationForm(FlaskForm):
    amount = DecimalField('Dollar Amount', places=2, validators=[NumberRange(min=0.01, message="Amount must be greater than 0")])
    donor_name = StringField('Donor Name', validators=[DataRequired()])
    donation_date = DateField('Date of Donation', format='%Y-%m-%d', default=date.today, validators=[Optional()])

class DistributionForm(FlaskForm):
    submit = SubmitField('Distribute')
