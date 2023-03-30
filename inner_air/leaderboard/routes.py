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
    usersConsecutive = User.query.order_by(User.consecutive_days.desc()).all()
    a = db.session.query(Statistics).join(User).filter(Statistics.exercise_id == 11).order_by(
        Statistics.hold_length.desc())
    usersHeld = db.session.query(Statistics, User).join(User).filter(Statistics.exercise_id == 11).order_by(
        Statistics.hold_length.desc()).limit(10).all()
    usersHeldDict = dict()
    for i, j in usersHeld:
        try:
            usersHeldDict[j.firstname] = usersHeldDict.get(j.firstname) + i.hold_length
        except:
            usersHeldDict[j.firstname] = i.hold_length

    return render_template('leaderboard/leaderboard.html', usersConsecutive=usersConsecutive,
                           usersHeldDict=usersHeldDict)
