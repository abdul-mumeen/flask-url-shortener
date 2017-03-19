from flask import Blueprint
#This Blueprint is instantiated here to prevent circular dependencies
main = Blueprint('main', __name__)
from . import views, errors
