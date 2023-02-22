from flask import Blueprint, render_template
from flask_login import login_required

from inner_air.utils.decorators import check_confirmed

main_bp = Blueprint(
    'main', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/%s' % __name__
)


@main_bp.route('/')
@main_bp.route('/home')
@login_required
@check_confirmed
def home():
    return render_template('main/index.html')
