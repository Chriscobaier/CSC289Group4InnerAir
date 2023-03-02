from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField


class RateEx(FlaskForm):
    RateField = RadioField(label='Rate this Exercise',
                           choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    submit = SubmitField(
        label='Submit'
    )
