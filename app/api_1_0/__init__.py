from flask import Blueprint
# This Blueprintis instantiated here so as to prevent circular dependencies
api = Blueprint('api', __name__)
from app.api_1_0 import authentication, url, user, errors, validators
