from flask import Blueprint, render_template
from flask_login import login_required

from inner_air.models import User
from inner_air.utils.decorators import check_confirmed

userlist_bp = Blueprint(
    'userlist', __name__,
    template_folder='templates'
)


@userlist_bp.route('/userlist', methods=['GET', 'POST'])
@login_required
@check_confirmed
def userlist():
    """
        I tried to create a table so that something can be displayed, nothing fancy.
    """
    users = User.query.all()
    return render_template('user_list/userlist.html', users=users)
