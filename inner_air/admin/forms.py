from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms import BooleanField, SelectField


class UserRecordForm(FlaskForm):
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
    submit = SubmitField(
        label='Update Record'
    )
