from flask import Blueprint, render_template
from flask_login import login_required

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
    return render_template('admin/admin.html')
