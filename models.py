from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
