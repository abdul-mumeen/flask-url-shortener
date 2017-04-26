from flask_inputs import Inputs
from wtforms.validators import URL, DataRequired, Email, EqualTo


class RegisterInputsValidator(Inputs):
    # This class is used to validate input submitted during signup
    json = {
        'email': [DataRequired(), Email()],
        'first_name': [DataRequired()],
        'last_name': [DataRequired()],
        'password': [DataRequired(), EqualTo('confirm_password',
                                             message='Password must match')],
        'confirm_password': [DataRequired()]
    }


class LongUrlValidator(Inputs):
    # This class is used to validate long url supplied
    json = {
        'long_url': [DataRequired(), URL()]
    }


class ShortUrlValidator(Inputs):
    # This class is used to validate a short url supplied
    json = {
        'short_url': [DataRequired(), URL()]
    }
