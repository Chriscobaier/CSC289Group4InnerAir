import flask_login
from flask import Blueprint, request, render_template
from flask_login import login_required

from inner_air import db
from inner_air.models import Favorites, Exercise, UserRating
from inner_air.utils.decorators import check_confirmed
from inner_air.exercises.forms import RateEx

exercises_bp = Blueprint(
    'exercises', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/%s' % __name__
)


@exercises_bp.route('/exercises', methods=['GET', 'POST'])
@login_required
@check_confirmed
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

    return render_template('exercises/exercises.html', exercises=exercise_list, favorites=favorite_list,
                           showFavAdd=showFav())


"""
    first_or_404() - returns the first result of the query or HTTP 404 Error.

    https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/api/#module-flask_sqlalchemy.pagination:~:text=Session%5D)%20%E2%80%93-,first_or_404,-(description%3D
"""


@exercises_bp.route('/exercises/<exid>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def get_exercise_id(exid):
    # Update cumulative ratings
    all_ex_data = db.session.query(UserRating).filter_by(exercise_id=exid).all()
    all_ex_data_count = len(all_ex_data)
    if all_ex_data_count > 0:
        all_ex_data_total = 0
        for i in all_ex_data:
            all_ex_data_total += i.user_rating
        cumulateData = all_ex_data_total / all_ex_data_count
        db.session.query(Exercise).filter_by(id=exid).first().update_cumulative_rating(cumulateData)
        db.session.commit()

    this_exercise = db.session.query(Exercise).filter_by(id=exid).first_or_404()
    form = RateEx()
    if form.validate():
        # Check if user has rated this before
        usersRating = db.session.query(UserRating).filter_by(user_id=flask_login.current_user.id, exercise_id=exid).first()
        if usersRating is None:
            usersRating = (UserRating(user_rating=int(form.RateField.data), user_id=flask_login.current_user.id, exercise_id=exid))
            db.session.add(usersRating)
        else:
            usersRating.update_rating(int(form.RateField.data))
        db.session.commit()

    return render_template('exercises/exerciseAnimation.html', this_exercise=this_exercise, form=form)
