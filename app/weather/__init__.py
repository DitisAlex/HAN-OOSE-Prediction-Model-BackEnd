from flask import Blueprint
bp = Blueprint('weather', __name__)
from . import routes