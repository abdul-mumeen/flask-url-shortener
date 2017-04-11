from flask_inputs import Inputs
from wtforms.validators import URL, DataRequired, Email, EqualTo


class RegisterInputs(Inputs):
    # This class is used to validate input submitted during signup
    json = {
        'email': [DataRequired(), Email()],
        'first_name': [DataRequired()],
        'last_name': [DataRequired()],
        'password': [DataRequired(), EqualTo('confirm_password',
                                             message='Password must match')],
        'confirm_password': [DataRequired()]
    }


class ValidateLongUrl(Inputs):
    # This class is used to validate long url supplied
    json = {
        'long_url': [DataRequired(), URL()]
    }


class ValidateShortUrl(Inputs):
    # This class is used to validate a short url supplied
    json = {
        'short_url': [DataRequired(), URL()]
    }
