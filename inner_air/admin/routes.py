from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

from inner_air.utils.decorators import check_confirmed

admin_bp = Blueprint(
    'admin', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/%s' % __name__
)


@admin_bp.route('/admin')
@login_required
@check_confirmed
def admin():
    if not current_user.is_admin:
        abort(403)

    return render_template('admin/admin.html')
