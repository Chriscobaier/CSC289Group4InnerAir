import pytest
from flask import Flask

from inner_air.models import User, Exercise, Routine, Favorites, Statistics, Category, UserRating, db

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '`5J<-lgHQaae_|LR*h)0%}`#k?sW@IK],P-9,A/}d`Ly&GwruSUh#omM]AdXwNP'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database per app config
db.init_app(app)

# Create all database tables
with app.app_context():
    db.create_all()


# Fixture, db session for this test
@pytest.fixture(scope="module")
def db_session():
    test_user = User(firstname="testUser", email="testUser@example.com", password="changeme")
    test_exercise = Exercise(exercise_name='test_exercise_name',
                             exercise_instructions='test_exercise_instructions',
                             exercise_description='test_exercise_descriptions',
                             exercise_length=12, category_id=1)
    test_user2 = User(firstname="testUser2", email="testUser2@example.com", password="changemetoo")
    test_exercise2 = Exercise(exercise_name='test_exercise_name2',
                              exercise_instructions='test_exercise_instructions2',
                              exercise_description='test_exercise_descriptions2',
                              exercise_length=12, category_id=1)
    with app.app_context():
        db.session.add(test_user)
        db.session.add(test_exercise)
        db.session.add(test_user2)
        db.session.add(test_exercise2)
        db.session.commit()
        yield db.session
        db.session.remove()


# Fixture for "current user" I am testing it this way because we will use a variable like this with the user is logged in
@pytest.fixture()
def current_user(db_session):
    currentUser = db.session.query(User).filter_by(email='testUser@example.com').one()
    return currentUser


# Fixture for "current exercise" I am testing it this way because we will use a variable like this with an exercise is selected
@pytest.fixture()
def current_exercise(db_session):
    currentExercise = db.session.query(Exercise).filter_by(exercise_name='test_exercise_name').one()
    return currentExercise


# Validate that we can find all users in a table
def test_multiple_users(db_session):
    counter = 0
    user_table = db.session.query(User).all()
    for user in user_table:
        counter += 1
        print('\n')
        print(user.as_dict())
    assert counter == 2


# Validate that we can find all exercises in a table
def test_multiple_exercises(db_session):
    counter = 0
    exercise_table = db.session.query(Exercise).all()
    for exercise in exercise_table:
        counter += 1
        print('\n')
        print(exercise.as_dict())
    assert counter == 2


# Test that we can query for user data on username
def test_user_model(db_session):
    test_user = db.session.query(User).filter_by(firstname='testUser').one()
    assert test_user.firstname == "testUser"
    assert test_user.email == "testUser@example.com"
    assert test_user.verify_password(attempted_password='changeme')
    print(f"\n Dictionary of User Object: {test_user.as_dict()} \n")


# Test that we can use the "current user object" and read its data
def test_user_fixture(current_user):
    assert current_user.firstname == "testUser"
    assert current_user.email == "testUser@example.com"
    assert current_user.verify_password(attempted_password='changeme')


# Test we can query db for exercise data
def test_exercise_model(db_session):
    test_exercise = db_session.query(Exercise).filter_by(exercise_name='test_exercise_name').one()
    assert test_exercise.exercise_name == 'test_exercise_name'
    assert test_exercise.exercise_instructions == 'test_exercise_instructions'
    assert test_exercise.exercise_description == 'test_exercise_descriptions'
    assert test_exercise.exercise_length == 12
    # assert test_exercise.cumulative_rating == 100 todo test later
    print(f"\n Dictionary of exercise Object: {test_exercise.as_dict()} \n")


# Test we can find exercise data based on object
def test_exercise_fixture(current_exercise):
    assert current_exercise.exercise_name == 'test_exercise_name'
    assert current_exercise.exercise_instructions == 'test_exercise_instructions'
    assert current_exercise.exercise_description == 'test_exercise_descriptions'
    assert current_exercise.exercise_length == 12


# Test we can find the user's routine
def test_routine_model(db_session):
    test_routine_add = Routine(user_id=db.session.query(User).first().id,
                               exercise_id=db.session.query(Exercise).first().id)
    db.session.add(test_routine_add)
    db.session.commit()
    test_routine_add2 = Routine(user_id=db.session.query(User).first().id,
                                exercise_id=db.session.query(Exercise).filter_by(
                                    exercise_name='test_exercise_name2').one().id)
    db.session.add(test_routine_add2)
    db.session.commit()
    test_routine = db.session.query(Routine).first()
    assert test_routine.id == db.session.query(User).first().id
    assert test_routine.id == db.session.query(Exercise).first().id
    print(f"\n Dictionary of Routine Object: {test_routine.as_dict()} \n")


# test pull all data / routines
def test_routine_list_all_routines(db_session, current_user):
    routine_table_for_user = db.session.query(Routine).filter_by(user_id=current_user.id).all()
    for exerciseID in routine_table_for_user:
        print(exerciseID.as_dict())


# Test pull all routines for one user, and join relevant tables for neat info
def test_routine_list_all_routines_with_join(db_session, current_user):
    results = (db_session.query(Routine, Exercise, User).filter(Routine.exercise_id == Exercise.id).filter(
        Routine.user_id == User.id).filter(Routine.user_id == current_user.id))
    for row in results:
        print(row.Routine.id, row.User.firstname, row.Exercise.exercise_name)


# Test add favorites
def test_favorites_model(db_session):
    test_favorites_add = Favorites(user_id=db.session.query(User).first().id,
                                   exercise_id=db.session.query(Exercise).first().id)
    db.session.add(test_favorites_add)
    db.session.commit()
    assert test_favorites_add.id == db.session.query(User).first().id
    assert test_favorites_add.id == db.session.query(Exercise).first().id
    print(f"\n Dictionary of Favorites Object: {test_favorites_add.as_dict()} \n")


# Test add new statistics
def test_statistics_model_new(db_session, current_user, current_exercise):
    # On exercise complete
    if db_session.query(Statistics).filter_by(user_id=current_user.id,
                                              exercise_id=current_exercise.id).first() is None:
        test_add_statistics = Statistics(exercises_completed=1, exercise_id=current_exercise.id,
                                         user_id=current_user.id)
        db.session.add(test_add_statistics)
        db.session.commit()

    # for actual code we need an else, but for this test it isn't needed as I am doing a new test here
    else:
        update_stats = db_session.query(Statistics).filter_by(user_id=current_user.id,
                                                              exercise_id=current_exercise.id).first()
        update_stats.exercises_completed += 1
        db.session.commit()
    assert db_session.query(Statistics).filter_by(user_id=current_user.id,
                                                  exercise_id=current_exercise.id).first().exercises_completed == 1
    print("\n Dictionary of Statistics Table:\n")
    statsTable = db_session.query(Statistics).all()
    for stat in statsTable:
        print(stat.as_dict())


# Test update statistics
def test_statistics_model_update(db_session, current_user, current_exercise):
    # On exercise complete
    if db_session.query(Statistics).filter_by(user_id=current_user.id,
                                              exercise_id=current_exercise.id).first() is None:
        test_add_statistics = Statistics(exercises_completed=1, exercise_id=current_exercise.id,
                                         user_id=current_user.id)
        db.session.add(test_add_statistics)
        db.session.commit()

    # for actual code we need an else, but for this test it isn't needed as I am doing a new test here
    else:
        update_stats = db_session.query(Statistics).filter_by(user_id=current_user.id,
                                                              exercise_id=current_exercise.id).first()
        update_stats.exercises_completed += 1
        db.session.commit()
    assert db_session.query(Statistics).filter_by(user_id=current_user.id,
                                                  exercise_id=current_exercise.id).first().exercises_completed == 2
    print("\n Dictionary of Statistics Table:\n")
    statsTable = db_session.query(Statistics).all()
    for stat in statsTable:
        print(stat.as_dict())


# Test add category
def test_category_model(db_session, current_user, current_exercise):
    test_category_add1 = Category(category_name='Inside Activity')
    test_category_add2 = Category(category_name='Outside Activity')
    db.session.add(test_category_add1)
    db.session.add(test_category_add2)
    db.session.commit()
    category_table = db.session.query(Category).all()
    for thing in category_table:
        print(thing.as_dict())
    pass


# test add new rating
def test_userRating_model_new(db_session, current_user, current_exercise):
    # Check if rating exists
    if db_session.query(UserRating).filter_by(user_id=current_user.id,
                                              exercise_id=current_exercise.id).first() is None:
        print("Does not exist, creating new")
        db.session.add(
            UserRating(user_rating=100, user_id=current_user.id, exercise_id=current_exercise.id))
        db.session.commit()
    else:
        rating_to_update = db_session.query(UserRating).filter_by(user_id=current_user.id,
                                                                  exercise_id=current_exercise.id).first()
        rating_to_update.user_rating = 90
        print('\n')
    print(db_session.query(UserRating).filter_by(user_id=current_user.id,
                                                 exercise_id=current_exercise.id).first().as_dict())
    assert db_session.query(UserRating).filter_by(user_id=current_user.id,
                                                  exercise_id=current_exercise.id).first().user_rating == 100


# test update user's rating
def test_userRating_model_update(db_session, current_user, current_exercise):
    # Check if rating exists
    if db_session.query(UserRating).filter_by(user_id=current_user.id,
                                              exercise_id=current_exercise.id).first() is None:
        print("Does not exist, creating new")
        db.session.add(
            UserRating(user_rating=100, user_id=current_user.id, exercise_id=current_exercise.id))
        db.session.commit()
    else:
        rating_to_update = db_session.query(UserRating).filter_by(user_id=current_user.id,
                                                                  exercise_id=current_exercise.id).first()
        rating_to_update.user_rating = 90
    print('\n')
    print(db_session.query(UserRating).filter_by(user_id=current_user.id,
                                                 exercise_id=current_exercise.id).first().as_dict())
    assert db_session.query(UserRating).filter_by(user_id=current_user.id,
                                                  exercise_id=current_exercise.id).first().user_rating == 90
