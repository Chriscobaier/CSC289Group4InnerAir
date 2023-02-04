import pytest
from models import User, Exercise, Routine, Favorites, Statistics, Category, UserRating, db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '`5J<-lgHQaae_|LR*h)0%}`#k?sW@IK],P-9,A/}d`Ly&GwruSUh#omM]AdXwNP'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()


@pytest.fixture(scope="module")
def db_session():
    test_user = User(firstname="testUser", email="testUser@example.com", password="changeme")
    test_exercise = Exercise(exercise_name='test_exercise_name',
                             exercise_instructions='test_exercise_instructions',
                             exercise_description='test_exercise_descriptions',
                             exercise_length=12, cumulative_rating=100, category_id=1)
    with app.app_context():
        db.session.add(test_user)
        db.session.add(test_exercise)
        db.session.commit()
        yield db.session
        db.session.remove()


def test_user_model(db_session):
    test_user = db.session.query(User).first()
    assert test_user.firstname == "testUser"
    assert test_user.email == "testUser@example.com"
    assert test_user.password == "changeme"
    print(f"\n Dictionary of User Object: {test_user.as_dict()} \n")


def test_exercise_model(db_session):
    test_exercise = db.session.query(Exercise).first()
    assert test_exercise.exercise_name == 'test_exercise_name'
    assert test_exercise.exercise_instructions == 'test_exercise_instructions'
    assert test_exercise.exercise_description == 'test_exercise_descriptions'
    assert test_exercise.exercise_length == 12
    assert test_exercise.cumulative_rating == 100
    print(f"\n Dictionary of exercise Object: {test_exercise.as_dict()} \n")


def test_routine_model(db_session):
    test_routine_add = Routine(user_id=db.session.query(User).first().userID,
                               exercise_id=db.session.query(Exercise).first().exerciseID)
    db.session.add(test_routine_add)
    db.session.commit()
    test_routine = db.session.query(Routine).first()
    assert test_routine.user_id == db.session.query(User).first().userID
    assert test_routine.exercise_id == db.session.query(Exercise).first().exerciseID
    print(f"\n Dictionary of Routine Object: {test_routine.as_dict()} \n")


def test_favorites_model(db_session):
    test_favorites_add = Favorites(user_id=db.session.query(User).first().userID,
                                   exercise_id=db.session.query(Exercise).first().exerciseID)
    db.session.add(test_favorites_add)
    db.session.commit()
    assert test_favorites_add.user_id == db.session.query(User).first().userID
    assert test_favorites_add.exercise_id == db.session.query(Exercise).first().exerciseID
    print(f"\n Dictionary of Favorites Object: {test_favorites_add.as_dict()} \n")


