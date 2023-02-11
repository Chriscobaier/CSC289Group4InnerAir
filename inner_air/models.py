from flask_login import UserMixin
from inner_air import bcrypt, login_manager

from inner_air import db


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'User.Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_time = db.Column(db.DateTime, default=db.func.current_timestamp())

    routines = db.relationship('Routine', backref='User', lazy=True)
    favorites = db.relationship('Favorites', backref='User', lazy=True)
    statistics = db.relationship('Statistics', backref='User', lazy=True)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def verify_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def updateLastLogin(self):
        todayDate = datetime.datetime.today()
        if self.last_login > (todayDate - datetime.timedelta(hours=24)):
            self.consecutive_days += 1
        else:
            self.consecutive_days = 0
        self.last_login = datetime.datetime.today()


class Exercise(db.Model):
    __tablename__ = 'Exercise.Details'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exercise_name = db.Column(db.String(64), nullable=False, unique=True)
    exercise_instructions = db.Column(db.String(256), nullable=False)
    exercise_description = db.Column(db.String(256), nullable=False)
    exercise_length = db.Column(db.Float, nullable=False)
    cumulative_rating = db.Column(db.Float)
    category_id = db.Column(db.Integer, nullable=False)
    user_rating_count = db.Column(db.Integer)

    routines = db.relationship('Routine', backref='Exercise', lazy=True)
    favorites = db.relationship('Favorites', backref='Exercise', lazy=True)
    statistics = db.relationship('Statistics', backref='Exercise', lazy=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Routine(db.Model):
    __tablename__ = 'Users.Routines'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.Users.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('Exercise.Details.id'), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Favorites(db.Model):
    __tablename__ = 'Users.Favorites'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.Users.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('Exercise.Details.id'), nullable=False)

    __table_args__ = (db.UniqueConstraint('user_id', 'exercise_id', name='UniqueUserExercise'),)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Statistics(db.Model):
    __tablename__ = 'Users.Statistics'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    date_completed = db.Column(db.DateTime, default=db.func.current_timestamp())
    exercise_id = db.Column(db.Integer, db.ForeignKey('Exercise.Details.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.Users.id'), nullable=False)
    hold_length = db.Column(db.Float)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Category(db.Model):
    __tablename__ = 'Exercise.Category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(50), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserRating(db.Model):
    __tablename__ = 'Exercise.UserRating'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_rating = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.Users.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('Exercise.Details.id'), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class DBVersion(db.Model):
    __tablename__ = 'App.Version'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    version = db.Column(db.String(12), nullable=False)
    load_time = db.Column(db.DateTime, default=db.func.current_timestamp())
