from flask import Flask, render_template, request, url_for, redirect

from models import User, UserInfo, Exercise, Routine, Favorites, Statistics, Category, UserRating, db

# from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import InputRequired, Length, ValidationError, Email
# from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = '`5J<-lgHQaae_|LR*h)0%}`#k?sW@IK],P-9,A/}d`Ly&GwruSUh#omM]AdXwNP'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# Comment out unless you are building a new database, for testing I am doing testv01.db etc etc

squareBreath = Exercise(exercise_name='Square Breathing',
                        exercise_instructions='Begin by exhaling and emptying all of the air from your lungs.  Then, inhale to a count of 4.  Hold this breath for a count of 4.  Exhale this breath with a count of 4, and hold your empty lungs for a count of 4.  Repeat.',
                        exercise_description='This is a useful breathing technique that is used to help calm your body. Try to use during stressful situations.',
                        exercise_length=6, user_rating=None, cumulative_rating=None, category_id=1)

squareBreath2 = Exercise(exercise_name='Square Breathing v2',
                         exercise_instructions='Begin by exhaling and emptying all of the air from your lungs.  Then, inhale to a count of 4.  Hold this breath for a count of 4.  Exhale this breath with a count of 6, and hold your empty lungs for a count of 2.  Repeat.',
                         exercise_description='A modified version of the Square Breathing method. The longer exhale activates the parasympathetic nervous system which slows your heart.  Try this before bed to help you relax.',

                         exercise_length=6, user_rating=None, cumulative_rating=None, category_id=1)




@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html")


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    pass


with app.app_context():
    db.session.add(squareBreath)
    db.session.add(squareBreath2)
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
