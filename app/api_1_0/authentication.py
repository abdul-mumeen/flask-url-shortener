from app.models import User
from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from . import api
from .errors import forbidden, unauthorized
from .validators import RegisterInputs

auth = HTTPTokenAuth(scheme='Token')
basic_auth = HTTPBasicAuth()


@api.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@api.before_request
@auth.login_required
def before_request():
    """
    This fun
    """
    if request.method != 'OPTIONS':
        allowed_anonymous_routes = ['token', 'register', 'shorten', 'recent',
                                    'popular', 'visit', 'influential']
        is_allowed_route = set(request.path.split('/')) \
            .intersection(set(allowed_anonymous_routes))
        if (g.current_user.is_anonymous and not is_allowed_route):
            return unauthorized('Invalid credentials')


@api.route('/register', methods=['POST'])
def register_user():
    """
    This function creates a new user from user information such as
    firt_name, Last_name, email and password delivered through the body of
    the request.
    """
    request_data = request.json or request.form
    inputs = RegisterInputs(request)
    if not inputs.validate():
        return forbidden(inputs.errors)
    if User.query.filter_by(email=request_data.get('email')).first():
        return forbidden('Email already exist.')
    user = User(first_name=request_data.get('first_name'),
                last_name=request_data.get('last_name'),
                email=request_data.get('email'),
                password=request_data.get('password'))
    user.save()
    response = jsonify(
        {'success': True, 'message': 'User creation successful'})
    response.status_code = 201
    return response


@api.route('/token')
@basic_auth.login_required
def get_token():
    """
    This function call the get_user_token function to return a token to the
    user after the username and passsword has been verified.
    """
    if g.current_user.is_anonymous:
        return forbidden('Supply a username and password')
    email = g.current_user.email
    user = User.query.filter_by(email=email).first()
    return get_user_token(user)


def get_user_token(user):
    """
    This function returns the generated user token.

    Keyword arguments:
    user -- this is the User object representing the current user
    """
    return jsonify({'token': user.generate_auth_token(
        expiration=3600).decode('utf-8'),
        'expiration': 3600})


@auth.verify_token
def verify_token(token):
    """
    This function verifies the token supplied by the user.

    Keyword arguments:
    token -- a string of encoded cheracters.
    """
    if not token:
        g.current_user = User.query.filter_by(
            email='anonymous@anonymous.com').first()
        if not g.current_user:
            g.current_user = User(
                first_name='anonymous', last_name='anonymous', anonymous=True,
                email='anonymous@anonymous.com', password='anonymous')
        g.current_user.anonymous = True
        return True
    g.current_user = User.verify_auth_token(token)
    return g.current_user is not None


@basic_auth.verify_password
def verify_password(email, password):
    """
    This function verifies the email and password supplied by the user.
    It initiates an anonymous user if no email is supplied.

    Keyword arguments:
    email -- an email address passed as string
    password -- a string variable
    """
    if not email:
        g.current_user = User.query.filter_by(
            email='anonymous@anonymous.com').first()
        if not g.current_user:
            g.current_user = User(
                first_name='anonymous', last_name='anonymous', anonymous=True,
                email='anonymous@anonymous.com', password='anonymous')
        g.current_user.anonymous = True
        return True
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)


@basic_auth.error_handler
@auth.error_handler
def auth_error():
    """
    This function returns unauthorized error when authentication fails.
    """
    return unauthorized('Invalid credentials')
