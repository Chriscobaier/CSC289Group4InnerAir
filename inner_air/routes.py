import flask_login
from inner_air import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
import json
from inner_air.forms import RegistrationForm, LoginForm
from inner_air.models import Exercise, User, Routine, Favorites, Statistics, Category, UserRating, DBVersion
from datetime import datetime, timedelta


def DeleteAndCreateDB():
    with app.app_context():
        try:
            thisVersion = db.session.query(DBVersion).order_by(DBVersion.version.desc()).first()
        except:
            thisVersion = None

        if thisVersion is None:
            db.drop_all()
            db.create_all()
            with open('importdata/data.json') as f:
                data = json.load(f)
                j = data["exercises"]
                for i in j:
                    db.session.add(Exercise(exercise_name=i["name"],
                                            exercise_instructions=i["exercise_instructions"],
                                            exercise_description=i["exercise_description"],
                                            exercise_length=i["exercise_length"], category_id=i["category_id"]))
                    db.session.commit()
                j = data["users"]
                for i in j:
                    db.session.add(User(firstname=i["firstname"],
                                        email=i["email"],
                                        password_hash=i["password_hash"],
                                        consecutive_days=i['consecutive_days']))
                for i in range(365):
                    x = datetime.today() - timedelta(days=i)
                    db.session.add(Statistics(date_completed=x, user_id=1, exercise_id=1))
                    db.session.commit()
                for i in range(45):
                    x = datetime.today() - timedelta(days=i)
                    db.session.add(Statistics(date_completed=x, user_id=2, exercise_id=1))
                    db.session.commit()
                for i in range(7):
                    x = datetime.today() - timedelta(days=i)
                    db.session.add(Statistics(date_completed=x, user_id=3, exercise_id=3))
                    db.session.commit()
            db.session.add(DBVersion(version='0.02'))
            db.session.commit()
        elif str(thisVersion.version) < '0.02':
            db.drop_all()
            db.create_all()
            with open('importdata/data.json') as f:
                data = json.load(f)
                j = data["exercises"]
                for i in j:
                    db.session.add(Exercise(exercise_name=i["name"],
                                            exercise_instructions=i["exercise_instructions"],
                                            exercise_description=i["exercise_description"],
                                            exercise_length=i["exercise_length"], category_id=i["category_id"]))
                    db.session.commit()
                j = data["users"]
                for i in j:
                    db.session.add(User(firstname=i["firstname"],
                                        email=i["email"],
                                        password_hash=i["password_hash"],
                                        consecutive_days=i['consecutive_days']))
                for i in range(365):
                    x = datetime.today() - timedelta(days=i)
                    db.session.add(Statistics(date_completed=x, user_id=1, exercise_id=1))
                    db.session.commit()
                for i in range(45):
                    x = datetime.today() - timedelta(days=i)
                    db.session.add(Statistics(date_completed=x, user_id=2, exercise_id=1))
                    db.session.commit()
                for i in range(7):
                    x = datetime.today() - timedelta(days=i)
                    db.session.add(Statistics(date_completed=x, user_id=3, exercise_id=3))
                    db.session.commit()
            db.session.add(DBVersion(version='0.02'))
            db.session.commit()


DeleteAndCreateDB()


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # Check if the request method is POST
    if request.method == 'POST':
        # Check if the request form contains "favoriteButton" key
        if "favoriteButton" in request.form:
            # Retrieve user and exercise IDs from the request form
            currentUser = request.form['user_id']
            currentExercise = request.form['exercise_id']
            # Check if the current combination of user and exercise IDs is already in the Favorites table
            if db.session.query(Favorites).filter(Favorites.user_id == currentUser).filter(
                    Favorites.exercise_id == currentExercise).first() is None:
                db.session.add(Favorites(user_id=currentUser, exercise_id=currentExercise))
                db.session.commit()

        # Check if the request form contains "favoriteButtonRemove" key
        elif "favoriteButtonRemove" in request.form:
            # Retrieve user and exercise IDs from the request for
            currentUser = request.form['user_id']
            currentExercise = request.form['exercise_id']
            # Check if the current combination of user and exercise IDs is in the Favorites table
            if db.session.query(Favorites).filter(Favorites.user_id == currentUser).filter(
                    Favorites.exercise_id == currentExercise).first() is not None:
                toDelete = db.session.query(Favorites).filter(Favorites.user_id == currentUser).filter(
                    Favorites.exercise_id == currentExercise).first()
                db.session.delete(toDelete)
                db.session.commit()
        else:
            pass
    # Retrieve all entries from the Exercise and Favorites tables
    exercise_list = Exercise.query.all()
    favorite_list = Favorites.query.all()

    # Define a function to show the exercises that the current user has in the Favorites table
    def showFav():
        listOfExerciseCurrentUserHasInFavorites = []
        for favorite in favorite_list:
            if favorite.as_dict()['user_id'] == flask_login.current_user.id:
                listOfExerciseCurrentUserHasInFavorites.append(favorite.as_dict()['exercise_id'])
        return listOfExerciseCurrentUserHasInFavorites

    xDataAll = db.session.query(Statistics).filter_by(user_id=flask_login.current_user.id).all()
    xData = []
    yData = []
    j = 0
    for i in xDataAll:
        j += 1
        xData.append(i.date_completed)
        # Need to count # of exercises per day
        yData.append(j)

    return render_template('profile.html', exercises=exercise_list, favorites=favorite_list, showFavAdd=showFav(),
                           xData=xData, yData=yData)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()

        if user and user.verify_password(attempted_password=form.password.data):
            login_user(user)
            user.updateLastLogin()
            flash(f'Success! You are logged in as: {user.firstname}', category='success')
            return redirect(url_for('profile'))
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
            login_user(user)
            flash(f'Account created successfully for {form.firstname.data}', category='success')
            return redirect(url_for('profile'))

        else:
            flash("This email already exists.  Try logging in, or register with a different email", category='danger')
    return render_template("register.html", form=form)


@app.route('/userlist', methods=['GET', 'POST'])
@login_required
def userlist():
    """
        I tried to create a table so that something can be displayed, nothing fancy.
    """
    users = User.query.all()
    return render_template('userlist.html', users=users)


@app.route('/exercises', methods=['GET', 'POST'])
@login_required
def exercises():
    # Check if the request method is POST
    if request.method == 'POST':
        # Check if the request form contains "favoriteButton" key
        if "favoriteButton" in request.form:
            # Retrieve user and exercise IDs from the request form
            currentUser = request.form['user_id']
            currentExercise = request.form['exercise_id']
            # Check if the current combination of user and exercise IDs is already in the Favorites table
            if db.session.query(Favorites).filter(Favorites.user_id == currentUser).filter(
                    Favorites.exercise_id == currentExercise).first() is None:
                db.session.add(Favorites(user_id=currentUser, exercise_id=currentExercise))
                db.session.commit()

        # Check if the request form contains "favoriteButtonRemove" key
        elif "favoriteButtonRemove" in request.form:
            # Retrieve user and exercise IDs from the request for
            currentUser = request.form['user_id']
            currentExercise = request.form['exercise_id']
            # Check if the current combination of user and exercise IDs is in the Favorites table
            if db.session.query(Favorites).filter(Favorites.user_id == currentUser).filter(
                    Favorites.exercise_id == currentExercise).first() is not None:
                toDelete = db.session.query(Favorites).filter(Favorites.user_id == currentUser).filter(
                    Favorites.exercise_id == currentExercise).first()
                db.session.delete(toDelete)
                db.session.commit()
        else:
            pass
    # Retrieve all entries from the Exercise and Favorites tables
    exercise_list = Exercise.query.all()
    favorite_list = Favorites.query.all()

    # Define a function to show the exercises that the current user has in the Favorites table
    def showFav():
        listOfExerciseCurrentUserHasInFavorites = []
        for favorite in favorite_list:
            if favorite.as_dict()['user_id'] == flask_login.current_user.id:
                listOfExerciseCurrentUserHasInFavorites.append(favorite.as_dict()['exercise_id'])
        return listOfExerciseCurrentUserHasInFavorites

    return render_template('exercises.html', exercises=exercise_list, favorites=favorite_list, showFavAdd=showFav())


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you\'ve been logged out', category='info')
    return redirect(url_for('home'))
