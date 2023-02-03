from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

# from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import InputRequired, Length, ValidationError, Email
# from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = '`5J<-lgHQaae_|LR*h)0%}`#k?sW@IK],P-9,A/}d`Ly&GwruSUh#omM]AdXwNP'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'User.Users'
    userID = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(128), nullable=False)
    created_time = db.Column(db.DateTime, default=db.func.current_timestamp())

    info = db.relationship('UserInfo', backref='user', lazy=True)
    routines = db.relationship('Routine', backref='user', lazy=True)
    favorites = db.relationship('Favorites', backref='user', lazy=True)
    statistics = db.relationship('Statistics', backref='user', lazy=True)


class UserInfo(db.Model):
    __tablename__ = 'User.Info'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('User.Users.userID'), nullable=False)
    firstname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)


class Exercise(db.Model):
    __tablename__ = 'Exercise.Details'
    exerciseID = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String(64), nullable=False, unique=True)
    exercise_instructions = db.Column(db.String(256), nullable=False)
    exercise_description = db.Column(db.String(256), nullable=False)
    exercise_length = db.Column(db.Float, nullable=False)
    user_rating = db.Column(db.Float)
    cumulative_rating = db.Column(db.Float)
    category_id = db.Column(db.Integer, nullable=False)

    routines = db.relationship('Routine', backref='exercise', lazy=True)
    favorites = db.relationship('Favorites', backref='exercise', lazy=True)
    statistics = db.relationship('Statistics', backref='exercise', lazy=True)


class Routine(db.Model):
    __tablename__ = 'Users.Routines'
    routine_id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('Exercise.Details.exerciseID'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.Users.userID'), nullable=False)


class Favorites(db.Model):
    __tablename__ = 'Users.Favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.Users.userID'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('Exercise.Details.exerciseID'), nullable=False)


class Statistics(db.Model):
    __tablename__ = 'Users.Statistics'
    id = db.Column(db.Integer, primary_key=True)
    exercises_completed = db.Column(db.Integer, nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('Exercise.Details.exerciseID'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.Users.userID'), nullable=False)


class Category(db.Model):
    __tablename__ = 'Exercise.Category'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)


class UserRating(db.Model):
    __tablename__ = 'Exercise.UserRaiting'
    id = db.Column(db.Integer, primary_key=True)
    user_rating = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.Users.userID'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('Exercise.Details.exerciseID'), nullable=False)


with app.app_context():
    db.create_all()

# Comment out unless you are building a new database, for testing I am doing testv01.db etc etc

squareBreath = Exercise(exercise_name='Square Breathing',
                        exercise_instructions='Begin by exhaling and emptying all of the air from your lungs.  Then, inhale to a count of 4.  Hold this breath for a count of 4.  Exhale this breath with a count of 4, and hold your empty lungs for a count of 4.  Repeat.',
                        exercise_description='This is a useful breathing technique that is used to help calm your body. Try to use during stressful situations.',
                        exercise_length=6, user_rating=None, cumulative_rating=None, category_id=1)

squareBreath2 = Exercise(exercise_name='Square Breathing v2',
                         exercise_instructions='Begin by exhaling and emptying all of the air from your lungs.  Then, inhale to a count of 4.  Hold this breath for a count of 4.  Exhale this breath with a count of 6, and hold your empty lungs for a count of 2.  Repeat.',
                         exercise_description='A modified version of the Square Breathing method. The longer exhale activates the parasympathetic nervous system which slows your heart.  Try this before bed to help you relax.',

                         exercise_length=6, user_rating=None, cumulative_rating=None, category_id=1)
with app.app_context():
    db.session.add(squareBreath)
    db.session.add(squareBreath2)

if __name__ == "__main__":
    app.run(debug=True)
