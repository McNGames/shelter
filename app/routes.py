
from urllib.parse import urlsplit

from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import func, and_, select
from sqlalchemy.exc import SQLAlchemyError

from app import app, db, login
from flask import render_template, flash, redirect, url_for, request, jsonify
from app.models import Donation, User
from app.forms import LoginForm, ItemDonationForm, FinancialDonationForm, DistributionForm
import sqlalchemy as sa

from app.utils import verify

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
@app.route('/donate_items', methods=['GET', 'POST'])
@login_required
def donate_items():
    form = ItemDonationForm()
    if not verify(form): #invalid post or get request
        return render_template('donate_items.html', form=form)
    else: #Valid post, update state
        new_donation = Donation(
            donation_type=form.donation_type.data,
            item_description=form.description.data,
            quantity=form.quantity.data,
            donor_name=form.donor_name.data,
            donation_date=form.donation_date.data,
            distribution_status=False
        )
        try:
            db.session.add(new_donation)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error(f"An error occurred: {e}")
            return "An error occurred while processing your request.", 500
        flash('Thank you for your donation!', 'success')
        return redirect(url_for('donate_items'))  # Redirect after successful donation

# Route to add a new donation
@app.route('/donate_money', methods=['GET', 'POST'])
@login_required
def donate_money():
    form = FinancialDonationForm()
    if not verify(form):  # invalid post or get request
        return render_template('donate_money.html', form=form)
    else: #add donation
        new_donation = Donation(
            donation_type='dollar',
            amount=form.amount.data,
            donor_name=form.donor_name.data,
            donation_date=form.donation_date.data,
            distribution_status=False
        )
        try:
            db.session.add(new_donation)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error(f"An error occurred: {e}")
            return "An error occurred while processing your request.", 500
        flash('Thank you for your donation!', 'success')
        return redirect(url_for('donate_money'))  # Redirect after successful donation

# Route to get all donations
@app.route('/distribute_donations', methods=['GET', 'POST'])
@login_required
def distribute_donations():
    form = DistributionForm()
    if not verify(form):  # invalid post or get request
        # Query to get money donations
        money_donos = db.session.query(Donation).filter(
            and_(
                Donation.distribution_status == False,
                Donation.donation_type == 'dollar'
            )
        ).order_by(Donation.donation_date.desc()).all()

        # Query to get item donations
        item_donos = db.session.query(Donation).filter(
            and_(
                Donation.distribution_status == False,
                Donation.donation_type != 'dollar'
            )
        ).order_by(Donation.donation_date.desc()).all()
        # TODO: Add pagination
        # Render the template with the fetched results
        return render_template('distribute_donations.html', form=form, money_donos=money_donos, item_donos=item_donos)
    else:
        selected_donations = request.form.getlist('donation_id')
        selected_donations_data = Donation.query.filter(Donation.id.in_(selected_donations)).all()
        for donation in selected_donations_data:
            donation.distribution_status = True
        db.session.commit()

        # Process the selected donations
        print(f'Selected donations: {selected_donations}')
        return redirect(url_for('distribute_donations'))  # Redirect after successful donation

# Route to get all donations
@app.route('/inventory_report', methods=['GET'])
@login_required
def inventory_report():
    item_donations = db.session.query(
        Donation.donation_type,
        Donation.distribution_status,
        func.sum(Donation.quantity).label('total_quantity')
    ).filter(
        Donation.donation_type != 'dollar'
    ).group_by(
        Donation.donation_type,
        Donation.distribution_status
    ).order_by(
        Donation.donation_type,
        Donation.distribution_status
    ).all()
    money_donations = db.session.query(
        Donation.distribution_status,
        func.sum(Donation.amount).label('total_amount')
    ).filter(
        Donation.donation_type == 'dollar'
    ).group_by(
        Donation.donation_type,
        Donation.distribution_status
    ).order_by(
        Donation.donation_type,
        Donation.distribution_status
    ).all()

    db.session.close()
    return render_template('inventory_report.html', item_donations=item_donations, money_donations=money_donations)

@app.route('/donor_report', methods=['GET'])
@login_required
def donor_report():
    donations = db.session.query(
        Donation.donor_name,
        Donation.donation_type,
        func.sum(Donation.quantity).label('total_quantity'),
        func.sum(Donation.amount).label('total_amount')
    ).group_by(
        Donation.donor_name,
        Donation.donation_type
    ).order_by(
        Donation.donor_name,
        Donation.donation_type,
    ).all()


    db.session.close()
    return render_template('donor_report.html', donations=donations)