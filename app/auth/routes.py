from flask import request, abort
from app.auth import bp
from app.auth.controller import AuthController


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    c = AuthController()

    try:
        return c.login("test", "test2")
    except KeyError:  # KeyError = missing key in json
        abort(401, "Invalid data")
