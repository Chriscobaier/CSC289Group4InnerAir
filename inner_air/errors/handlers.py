from flask import Blueprint, render_template

errors = Blueprint(
    'errors', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/%s' % __name__
)


@errors.app_errorhandler(401)
def unauthorized_page(error):
    return render_template("errors/401.html"), 401


@errors.app_errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403


@errors.app_errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@errors.app_errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500
