from flask import Blueprint

convert_api = Blueprint('convert_api', __name__)

from . import views
