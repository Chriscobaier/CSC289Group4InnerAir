from flask import Flask, render_template, request, url_for, redirect, flash

from models import User, Exercise, Routine, Favorites, Statistics, Category, UserRating, db
from forms import RegistrationForm

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


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created successfully for {form.firstname.data}', category='success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    pass


if __name__ == "__main__":
    app.run(debug=True)
