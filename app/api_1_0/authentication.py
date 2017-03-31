from flask_login import AnonymousUserMixin
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth
from .errors import forbidden, unauthorized
from . import api
from app.models import User
from flask import g, jsonify, request
from .validators import RegisterInputs
import json
auth = HTTPTokenAuth(scheme='Token')
basic_auth = HTTPBasicAuth()


@api.before_request
@auth.login_required
def before_request():
    if (g.current_user.is_anonymous
            and not set(request.path.split('/'))
            .intersection(set(['token', 'register', 'shorten', 'recent']))):
        return unauthorized('Invalid credentials')


@api.route('/register', methods=['POST'])
def register_user():
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
    response = jsonify({'success': True, 'message': 'User creation successful'})
    response.status_code = 200
    return response


@api.route('/token')
@basic_auth.login_required
def get_token():
    if g.current_user.is_anonymous:
        return forbidden('Supply a username and password')
    email = g.current_user.email
    user = User.query.filter_by(email=email).first()
    return get_user_token(user)


def get_user_token(user):
    return jsonify({'token': user.generate_auth_token(expiration=3600).decode('utf-8'),
                    'expiration': 3600})


@auth.verify_token
def verify_token(token):
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
    return unauthorized('Invalid credentials')
