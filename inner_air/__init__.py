from decouple import config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(config('APP_SETTINGS', default='inner_air.config.DevelopmentConfig'))

login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
migrate = Migrate(app, db)

"""
    registering blueprints
"""
from .main.routes import main_bp
from .user.routes import user_bp
from .profile.routes import profile_bp
from .exercises.routes import exercises_bp
from .user_list.routes import userlist_bp
from .errors.handlers import errors

app.register_blueprint(main_bp, url_prefix='/')
app.register_blueprint(user_bp, url_prefix='/')
app.register_blueprint(profile_bp, url_prefix='/')
app.register_blueprint(exercises_bp, url_prefix='/')
app.register_blueprint(userlist_bp, url_prefix='/')
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

