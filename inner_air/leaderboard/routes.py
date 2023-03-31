from flask import Blueprint, render_template
from inner_air.utils.decorators import check_confirmed
from flask_login import login_required

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
    return render_template('leaderboard/leaderboard.html')
