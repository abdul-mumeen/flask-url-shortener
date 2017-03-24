from flask import Blueprint
# This Blueprintis instantiated here so as to prevent circular dependencies
api = Blueprint('api', __name__)
from . import authentication, url, user, visitor, errors, validators
