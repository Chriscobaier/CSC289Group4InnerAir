from flask import Blueprint, render_template
from flask_login import login_required

from inner_air import User
from inner_air.models import Exercise, Statistics, Routine, Favorites, Category, UserRating, DBVersion
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
@admin_bp.route('/admin/tables')
@login_required
@check_confirmed
def tables():
    users_table = User.query.all()
    exercise_table = Exercise.query.all()
    routine_table = Routine.query.all()
    favorites_table = Favorites.query.all()
    statistics_table = Statistics.query.all()
    category_table = Category.query.all()
    user_rating_table = UserRating.query.all()
    db_version_table = DBVersion.query.all()

    return render_template('tables/tables.html',
                           users_table=users_table, exercise_table=exercise_table,
                           routine_table=routine_table, favorites_table=favorites_table,
                           statistics_table=statistics_table, category_table=category_table,
                           user_rating_table=user_rating_table, db_version_table=db_version_table
                           )
