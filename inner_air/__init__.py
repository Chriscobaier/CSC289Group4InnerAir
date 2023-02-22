from decouple import config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

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
from .main.routes import main_bp
from .user.routes import user_bp
from .profile.routes import profile_bp
from .exercises.routes import exercises_bp
from .user_list.routes import userlist_bp
from .errors.handlers import errors

app.register_blueprint(main_bp)
app.register_blueprint(user_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(exercises_bp)
app.register_blueprint(userlist_bp)
app.register_blueprint(errors)

"""
    flask-login
"""
from inner_air.models import User

login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


"""
    DB creation
"""
from inner_air import create_and_delete

