from flask_inputs import Inputs
from wtforms.validators import URL, DataRequired, Email, EqualTo

from .errors import forbidden


class RegisterInputs(Inputs):
    json = {
        'email': [DataRequired(), Email()],
        'first_name': [DataRequired()],
        'last_name': [DataRequired()],
        'password': [DataRequired(), EqualTo('confirm_password',
                                             message='Password must match')],
        'confirm_password': [DataRequired()]
    }


class ValidateLongUrl(Inputs):
    json = {
        'long_url': [DataRequired(), URL()]
    }


class ValidateShortUrl(Inputs):
    json = {
        'short_url': [DataRequired(), URL()]
    }
