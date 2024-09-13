from urllib.parse import urlsplit

from flask_login import current_user, login_user, logout_user, login_required

from app import app, db, login
from flask import render_template, flash, redirect, url_for, request, jsonify
from app.models import Donation, User
from app.forms import LoginForm
import sqlalchemy as sa

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# Route to add a new donation
@app.route('/add_donation', methods=['POST'])
def add_donation():
    data = request.get_json()
    donor_name = data.get('donor_name')
    donation_type = data.get('donation_type')
    item_description = data.get('item_description', None)
    quantity = data.get('quantity', None)
    amount = data.get('amount', None)

    # Validation for donation type
    if donation_type not in ['item', 'dollar']:
        return jsonify({'error': 'Invalid donation type'}), 400

    # Create a new Donation record
    new_donation = Donation(
        donor_name=donor_name,
        donation_type=donation_type,
        item_description=item_description,
        quantity=quantity,
        amount=amount
    )
    db.session.add(new_donation)
    db.session.commit()

    return jsonify(new_donation.to_dict()), 201

# Route to get all donations
@app.route('/donations', methods=['GET'])
def get_donations():
    donations = Donation.query.all()
    return jsonify([donation.to_dict() for donation in donations])

# Route to get a specific donation by ID
@app.route('/donations/<int:donation_id>', methods=['GET'])
def get_donation(donation_id):
    donation = Donation.query.get(donation_id)
    if donation is None:
        return jsonify({'error': 'Donation not found'}), 404
    return jsonify(donation.to_dict())