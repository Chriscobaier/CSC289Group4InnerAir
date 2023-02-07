from inner_air import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required

from inner_air.forms import RegistrationForm, LoginForm
from inner_air.models import Exercise, User, Routine, Favorites, Statistics, Category, UserRating, DBVersion


# COMMENT THIS OUT IF YOU DON'T WANT TO DELETE YOUR DATABASE
def DeleteAndCreateDB():
    with app.app_context():
        db.drop_all()
        db.create_all()
        for i in range(10):
            db.session.add(Exercise(exercise_name='test_exercise_name' + f' {i}',
                                    exercise_instructions='test_exercise_instructions' + f' {i}',
                                    exercise_description='test_exercise_descriptions' + f' {i}',
                                    exercise_length=12, category_id=1))
            db.session.commit()


# COMMENT THIS OUT IF YOU DON'T WANT TO DELETE YOUR DATABASE
# COMMENT THIS OUT IF YOU DON'T WANT TO DELETE YOUR DATABASE
# COMMENT THIS OUT IF YOU DON'T WANT TO DELETE YOUR DATABASE
DeleteAndCreateDB()


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
        user = User(
            firstname=form.firstname.data,
            email=form.email.data,
            password=form.password.data)  # Get user input from Registration form
        # Add user input to database

        if db.session.query(User).filter_by(email=form.email.data).first() is None:
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
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


@app.route('/exercises', methods=['GET', 'POST'])
def exercises():
    if request.method == 'POST':
        if "favoriteButton" in request.form:
            currentUser = request.form['user_id']
            currentExercise = request.form['exercise_id']
            if db.session.query(Favorites).filter(Favorites.user_id == currentUser).filter(
                    Favorites.exercise_id == currentExercise).first() is None:
                db.session.add(Favorites(user_id=currentUser, exercise_id=currentExercise))
                db.session.commit()
            else:
                flash("This is already a favorite, TODO REMOVE BUTTON IF ALREADY FAVORITE", category='danger')
        elif "routineButton" in request.form:
            pass
        else:
            pass
    exercise_list = Exercise.query.all()
    favorite_list = Favorites.query.all()
    return render_template('exercises.html', exercises=exercise_list, favorites=favorite_list)


@app.route('/logout')
def logout():
    logout_user()
    flash('you\'ve been logged out', category='info')
    return redirect(url_for('home'))
