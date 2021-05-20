from flask import Blueprint
bp = Blueprint('prediction', __name__)
from . import routes