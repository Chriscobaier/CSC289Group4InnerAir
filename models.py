from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'User.Users'
    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    created_time = db.Column(db.DateTime, default=db.func.current_timestamp())

    routines = db.relationship('Routine', backref='user', lazy=True)
    favorites = db.relationship('Favorites', backref='user', lazy=True)
    statistics = db.relationship('Statistics', backref='user', lazy=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Exercise(db.Model):
    __tablename__ = 'Exercise.Details'
    exerciseID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exercise_name = db.Column(db.String(64), nullable=False, unique=True)
    exercise_instructions = db.Column(db.String(256), nullable=False)
    exercise_description = db.Column(db.String(256), nullable=False)
    exercise_length = db.Column(db.Float, nullable=False)
    cumulative_rating = db.Column(db.Float)
    category_id = db.Column(db.Integer, nullable=False)

    routines = db.relationship('Routine', backref='exercise', lazy=True)
    favorites = db.relationship('Favorites', backref='exercise', lazy=True)
    statistics = db.relationship('Statistics', backref='exercise', lazy=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Routine(db.Model):
    __tablename__ = 'Users.Routines'
    routineid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.Users.userID'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('Exercise.Details.exerciseID'), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Favorites(db.Model):
    __tablename__ = 'Users.Favorites'
    favoritesid = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('User.Users.userID'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('Exercise.Details.exerciseID'), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Statistics(db.Model):
    __tablename__ = 'Users.Statistics'
    statisticsid = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    exercises_completed = db.Column(db.Integer, nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('Exercise.Details.exerciseID'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.Users.userID'), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Category(db.Model):
    __tablename__ = 'Exercise.Category'
    categoryid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(50), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserRating(db.Model):
    __tablename__ = 'Exercise.UserRaiting'
    userratingid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_rating = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.Users.userID'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('Exercise.Details.exerciseID'), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
