from flask import Blueprint, render_template
from inner_air.utils.decorators import check_confirmed
from flask_login import login_required
from inner_air.models import User, Statistics, Exercise
from inner_air import db

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
    usersConsecutive = User.query.order_by(User.consecutive_days.desc()).limit(10).all()

    # Assumes control pause is exercise 11 (could be problematic if it isn't)
    # Query statistics table, join User table, only get data where exercise is control pause, top 10 values
    usersHeld = db.session.query(Statistics, User).join(User).filter(Statistics.exercise_id == 11).order_by(
        Statistics.hold_length.desc()).limit(10).all()
    usersHeldMax = []
    for i, j in usersHeld:
        usersHeldMax.append({j.firstname: i.hold_length})
    # Get all breath hold data
    usersHeldTotal = db.session.query(Statistics, User).join(User).filter(Statistics.exercise_id == 11).order_by(
        Statistics.hold_length.desc()).all()
    usersHeldDict = dict()
    for i, j in usersHeldTotal:
        try:
            usersHeldDict[j.firstname] = usersHeldDict.get(j.firstname) + i.hold_length
        except:
            usersHeldDict[j.firstname] = i.hold_length

    return render_template('leaderboard/leaderboard.html', usersConsecutive=usersConsecutive,
                           usersHeldDict=usersHeldDict, usersHeldMax=usersHeldMax)
