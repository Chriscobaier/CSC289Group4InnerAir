import datetime

import flask_login
from flask import Blueprint, request, render_template

from inner_air import db
from inner_air.models import Favorites, Exercise, Statistics
from inner_air.utils.decorators import check_confirmed
from collections import OrderedDict

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

    # This can probably be improved.
    # Create list, and dictionary for three graphs
    xDataWeek = []
    xDataMonth = []
    xDataQ = []
    xDataWeekDict = dict()
    xDataMonthDict = dict()
    xDataQDict = dict()

    # Create dictionary for each range with 0 exercises
    # TODO Should use one for loop with 3 if statements to make it more efficient
    for i in range(7):
        j = datetime.date.today() - datetime.timedelta(days=i)
        xDataWeek.append(j)
        xDataWeekDict[j] = 0

    for i in range(31):
        j = datetime.date.today() - datetime.timedelta(days=i)
        xDataMonth.append(j)
        xDataMonthDict[j] = 0

    for i in range(91):
        j = datetime.date.today() - datetime.timedelta(days=i)
        xDataQ.append(j)
        xDataQDict[j] = 0

    # Receive all statistic data for ~92 days (prevent long term app querying too much data which can lead to slow load times)
    xDataAll = db.session.query(Statistics).filter_by(user_id=flask_login.current_user.id).filter(
        Statistics.date_completed >= (datetime.date.today() - datetime.timedelta(days=92))).all()

    # Make a list of the previous query which combines exercises that have occurred on same day
    xDataDates = []
    for i in xDataAll:
        xDataDates.append(i.date_completed.date())
    xDataDates.sort()
    exercisePerDay = {x: xDataDates.count(x) for x in xDataDates}

    # Loop previous dictionary and update the blank values with actual values for the dictionary
    for key, value in exercisePerDay.items():
        if key in xDataWeek:
            xDataWeekDict[key] = value
        if key in xDataMonth:
            xDataMonthDict[key] = value
        if key in xDataQ:
            xDataQDict[key] = value

    # More lists!
    # Probably a more efficient way for this, but if we sort the dictionary and iterate the key/value into two lists
    # we can populate this into charJS axis
    xDataWeekList = []
    xDataMonthList = []
    xDataQuarterList = []
    yDataWeek = []
    yDataMonth = []
    yDataQ = []
    xDataWeekDictSorted = OrderedDict(sorted(xDataWeekDict.items()))
    xDataMonthDictSorted = OrderedDict(sorted(xDataMonthDict.items()))
    xDataQDictSorted = OrderedDict(sorted(xDataQDict.items()))

    for key, value in xDataWeekDictSorted.items():
        xDataWeekList.append(key)
        yDataWeek.append(value)
    for key, value in xDataMonthDictSorted.items():
        xDataMonthList.append(key)
        yDataMonth.append(value)
    for key, value in xDataQDictSorted.items():
        xDataQuarterList.append(key)
        yDataQ.append(value)
    return render_template('profile/profile.html', exercises=exercise_list, favorites=favorite_list,
                           showFavAdd=showFav(),
                           xDataWeekList=xDataWeekList, yDataWeek=yDataWeek, xDataMonthList=xDataMonthList,
                           yDataMonth=yDataMonth, xDataQuarterList=xDataQuarterList, yDataQ=yDataQ)
