from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user

from inner_air import db
from inner_air.admin.forms import UserRecordForm
from inner_air.models import User
from inner_air.utils.decorators import check_confirmed

admin_bp = Blueprint(
    'admin', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/%s' % __name__
)


@admin_bp.route('/admin', methods=['GET', 'POST'])
@login_required
@check_confirmed
def admin():
    users = User.query.all()
    if not current_user.is_admin:
        abort(403)

    return render_template('admin/admin.html', users=users)


@admin_bp.route('/admin/update/<int:id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def update(id):
    form = UserRecordForm()
    user = db.session.query(User).get_or_404(id)

    if not current_user.is_admin:
        abort(403)

    if form.validate_on_submit():
        user.firstname = request.form['firstname']
        user.email = request.form['email']

        if user.is_confirmed:
            user.is_confirmed = False

        try:
            db.session.commit()
            flash('User Updated Successfully!', category='success')
            return render_template('includes/update.html', form=form, user=user)
        except Exception:
            flash('An error occurred...try again.', category='danger')
            return render_template('includes/update.html', form=form, user=user)
    else:
        return render_template('includes/update.html', form=form, user=user)


@admin_bp.route('/admin/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def delete(id):
    user = db.session.query(User).get_or_404(id)

    if not current_user.is_admin:
        abort(403)

    try:
        db.session.delete(user)
        db.session.commit()

        flash('User deleted successfully!', category='success')
        user = User.query.order_by(User.created_time)

        return redirect(url_for('admin.admin'))
    except Exception:
        flash('An error occurred...try again.', category='danger')
        return redirect(url_for('admin.admin'))
