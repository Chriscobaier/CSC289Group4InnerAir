from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegistrationForm(FlaskForm):
    firstname = StringField(
        label='First Name',
        validators=[DataRequired(), Length(max=64)],
        render_kw={"placeholder": "First Name"}
    )
    email = StringField(
        label='Email',
        validators=[DataRequired(), Email()],
        render_kw={'placeholder': 'Email'}
    )
    password = PasswordField(
        label='Password',
        validators=[DataRequired(), Length(min=8)],
        render_kw={"placeholder": "Password"}
    )
    confirm_password = PasswordField(
        label='Confirm Password',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={'placeholder': 'Confirm Password'}
    )
    submit = SubmitField(
        label='Sign up'
    )


class LoginForm(FlaskForm):
    email = StringField(
        label='Email',
        validators=[DataRequired(), Email()],
        render_kw={'placeholder': 'Email'}
    )
    password = PasswordField(
        label='Password',
        validators=[DataRequired()],
        render_kw={"placeholder": "Password"}
    )
    submit = SubmitField(
        label='Login'
    )


class ForgotForm(FlaskForm):
    email = StringField(
        label='Email',
        validators=[DataRequired(), Email()],
        render_kw={'placeholder': 'Email'}
    )
    submit = SubmitField(
        label='Request Password Reset'
    )


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        label='Password',
        validators=[DataRequired(), Length(min=8)],
        render_kw={"placeholder": "Password"}
    )
    confirm_password = PasswordField(
        label='Confirm Password',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={'placeholder': 'Confirm Password'}
    )
    submit = SubmitField(
        label='Reset Password'
    )


"""""
    update user profile - form
"""""


class ProfileForm(FlaskForm):
    firstname = StringField(
        label='First Name',
        validators=[DataRequired(), Length(max=64)],
    )
    profile_picture = FileField(
        label='Edit',
        validators=[FileAllowed(['jpg', 'png'])],
    )
    anonymous_mode = BooleanField('Anonymous Mode (Do not show on leaderboards)')

    submit = SubmitField(
        label='Update Profile',
    )


class EmailForm(FlaskForm):
    email = StringField(
        label='Email',
        validators=[DataRequired(), Email()],
        render_kw={'placeholder': 'Email'}
    )
    submit = SubmitField(
        label='Update Email'
    )


class SecurityAndAuthForm(FlaskForm):
    password = PasswordField(
        label='New Password',
        validators=[DataRequired(), Length(min=8)],
        render_kw={"placeholder": "New Password"}
    )
    confirm_password = PasswordField(
        label='Confirm New Password',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={'placeholder': 'Confirm New Password'}
    )
    submit = SubmitField(
        label='Update Password'
    )
