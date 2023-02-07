from inner_air import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required

from inner_air.forms import RegistrationForm, LoginForm
from inner_air.models import Exercise, User, Routine, Favorites, Statistics, Category, UserRating, DBVersion


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()

        if user and user.verify_password(password=form.password.data):
            login_user(user)
            flash(f'Success! You are logged in as: {user.firstname}', category='success')
            return redirect(url_for('dashboard'))
        else:
            flash('You have entered an invalid email address or password.', category='danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Return the register.html page"""
    form = RegistrationForm()
    if form.validate_on_submit():
        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Encrypt password

        user = User(
            firstname=form.firstname.data,
            email=form.email.data,
            password=encrypted_password)  # Get user input from Registration form
        # Add user input to database

        if db.session.query(User).filter_by(email=form.email.data).first() is None:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash(f'Account created successfully for {form.firstname.data}', category='success')
            return redirect(url_for('login'))

        else:
            flash("This email already exists.  Try logging in, or register with a different email", category='danger')
    return render_template("register.html", form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """
        I tried to create a table so that something can be displayed, nothing fancy.
    """
    users = User.query.all()
    return render_template('dashboard.html', users=users)


@app.route('/logout')
def logout():
    logout_user()
    flash('you\'ve been logged out', category='info')
    return redirect(url_for('home'))
