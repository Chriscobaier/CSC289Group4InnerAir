from flask import Flask, render_template
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from decouple import config


app = Flask(__name__)
app.config.from_object(config('APP_SETTINGS'))

login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

"""
    registering blueprints
"""
from inner_air.main.routes import main_bp
from inner_air.user.routes import user_bp
from inner_air.profile.routes import profile_bp
from inner_air.exercises.routes import exercises_bp
from inner_air.user_list.routes import userlist_bp

app.register_blueprint(main_bp)
app.register_blueprint(user_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(exercises_bp)
app.register_blueprint(userlist_bp)


"""
    flask-login
"""
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'


"""
    DB creation
"""
from inner_air import create_and_delete


"""
    error handlers
"""
@app.errorhandler(401)
def unauthorized_page(error):
    return render_template("errors/401.html"), 401


@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500
