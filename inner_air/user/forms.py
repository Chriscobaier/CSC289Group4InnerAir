from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegistrationForm(FlaskForm):
    firstname = StringField(
        label='First Name',
        validators=[DataRequired(), Length(min=3, max=20)],
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
