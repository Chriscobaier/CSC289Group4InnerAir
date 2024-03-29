from decouple import config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config('APP_SETTINGS'))

login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
migrate = Migrate(app, db)

"""
    User model
"""
from inner_air.models import User

"""
    registering blueprints
"""
from .admin.routes import admin_bp
from .main.routes import main_bp
from .user.routes import user_bp
from .profile.routes import profile_bp
from .exercises.routes import exercises_bp
from .leaderboard.routes import leaderboard_bp
from .errors.handlers import errors


app.register_blueprint(admin_bp, url_prefix='/')
app.register_blueprint(main_bp, url_prefix='/')
app.register_blueprint(user_bp, url_prefix='/')
app.register_blueprint(profile_bp, url_prefix='/')
app.register_blueprint(exercises_bp, url_prefix='/')
app.register_blueprint(leaderboard_bp, url_prefix='/')
app.register_blueprint(errors)

"""
    flask-login
"""
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


"""
    DB creation
"""
from inner_air import create_and_delete
