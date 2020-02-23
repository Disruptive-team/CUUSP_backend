from flask import Blueprint

api = Blueprint('api', __name__)

from .authentication import *
from .microservice import *
from .manage import *
