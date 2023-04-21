from flask import Blueprint, render_template
from inner_air.utils.decorators import check_confirmed
from flask_login import login_required
from inner_air.models import User, Statistics, Exercise
from inner_air import db
from sqlalchemy import func

from collections import OrderedDict

leaderboard_bp = Blueprint(
    'leaderboard', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/%s' % __name__
)


@leaderboard_bp.route('/leaderboard')
@login_required
@check_confirmed
def leaderboard():
    # Get all user's consecutive day values, simple list
    usersConsecutive = User.query.filter(User.is_anonymous == 0).order_by(User.consecutive_days.desc()).limit(10).all()

    # Assumes control pause is exercise 11 (could be problematic if it isn't)
    # Query statistics table, join User table, only get data where exercise is control pause, top 10 values
    usersHeld = db.session.query(Statistics, User).join(User).filter(Statistics.exercise_id == 11,
                                                                     User.is_anonymous == 0).order_by(
        Statistics.hold_length.desc()).limit(10).all()
    usersHeldMax = []
    for i, j in usersHeld:
        usersHeldMax.append({j: i.hold_length})

    # Get all breath hold data
    usersHeldTotal = db.session.query(Statistics, User).join(User).filter(Statistics.exercise_id == 11,
                                                                          User.is_anonymous == 0).order_by(
        Statistics.hold_length.desc()).all()
    usersHeldDict = dict()

    for i, j in usersHeldTotal:
        if i.user_id != 7:
            try:
                usersHeldDict[j] = usersHeldDict.get(j) + i.hold_length
            except:
                usersHeldDict[j] = i.hold_length
    tempList = sorted(usersHeldDict.items(), key=lambda x: x[1], reverse=True)
    usersHeldOrderedDict = dict(tempList)

    usersHeldOrderedList = list(usersHeldOrderedDict)

    usersNumberOfExercises = db.session.query(User, func.count(Statistics.id)).join(Statistics,
                                                                                    User.id == Statistics.user_id).group_by(
        User.id).filter(User.is_anonymous == 0).order_by(func.count(Statistics.id).desc()).limit(10).all()
    usersNumberOfExercisesList = []
    for i, j in usersNumberOfExercises:
        usersNumberOfExercisesList.append(i.firstname)

    return render_template('leaderboard/leaderboard.html', usersConsecutive=usersConsecutive,
                           usersHeldDict=usersHeldOrderedDict, usersHeldMax=usersHeldMax,
                           usersHeldOrderedList=usersHeldOrderedList, usersNumberOfExercises=usersNumberOfExercises,
                           usersNumberOfExercisesList=usersNumberOfExercisesList)
