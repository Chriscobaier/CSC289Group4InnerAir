import datetime

import flask_login
from flask import Blueprint, request, render_template

from inner_air import db
from inner_air.models import Favorites, Exercise, Statistics
from inner_air.utils.decorators import check_confirmed

profile_bp = Blueprint(
    'profile', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/%s' % __name__
)


@profile_bp.route('/profile', methods=['GET', 'POST'])
@check_confirmed
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
                db.session.add(Favorites(user_id=currentUser,
                                         exercise_id=currentExercise))
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
                listOfExerciseCurrentUserHasInFavorites.append(
                    favorite.as_dict()['exercise_id'])
        return listOfExerciseCurrentUserHasInFavorites

    xDataWeek = []
    xDataWeekDict = dict()
    xDataMonthDict = dict()
    xDataQDict = dict()
    for i in range(7):
        j = datetime.date.today() - datetime.timedelta(days=i)
        xDataWeek.append(j)
        xDataWeekDict[j] = 0
    xDataMonth = []
    for i in range(31):
        j = datetime.date.today() - datetime.timedelta(days=i)
        xDataMonth.append(j)
        xDataMonthDict[j] = 0
    xDataQ = []
    for i in range(91):
        j = datetime.date.today() - datetime.timedelta(days=i)
        xDataQ.append(j)
        xDataQDict[j] = 0

    xDataAll = db.session.query(Statistics).filter_by(user_id=flask_login.current_user.id).all()

    xDataDates = []
    for i in xDataAll:
        xDataDates.append(i.date_completed.date())
    xDataDates.sort()
    exercisePerDay = {x: xDataDates.count(x) for x in xDataDates}

    for key, value in exercisePerDay.items():
        if key in xDataWeek:
            xDataWeekDict[key] = value
        if key in xDataMonth:
            xDataMonthDict[key] = value
        if key in xDataQ:
            xDataQDict[key] = value
    xDataWeekList = []
    xDataMonthList = []
    xDataQuarterList = []
    yDataWeek = []
    yDataMonth = []
    yDataQ = []
    for key, value in xDataWeekDict.items():
        xDataWeekList.append(key)
        yDataWeek.append(value)
    for key, value in xDataMonthDict.items():
        xDataMonthList.append(key)
        yDataMonth.append(value)
    for key, value in xDataQDict.items():
        xDataQuarterList.append(key)
        yDataQ.append(value)
    return render_template('profile/profile.html', exercises=exercise_list, favorites=favorite_list,
                           showFavAdd=showFav(),
                           xDataWeekList=xDataWeekList, yDataWeek=yDataWeek, xDataMonthList=xDataMonthList,
                           yDataMonth=yDataMonth, xDataQuarterList=xDataQuarterList, yDataQ=yDataQ)
