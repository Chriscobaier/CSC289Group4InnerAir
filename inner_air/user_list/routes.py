from flask import Blueprint, render_template
from flask_login import login_required

from inner_air.models import User

userlist_bp = Blueprint(
    'userlist', __name__,
    template_folder='templates'
)


@userlist_bp.route('/userlist', methods=['GET', 'POST'])
@login_required
def userlist():
    """
        I tried to create a table so that something can be displayed, nothing fancy.
    """
    users = User.query.all()
    return render_template('userlist.html', users=users)
