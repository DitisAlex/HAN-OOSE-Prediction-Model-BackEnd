import os

from flask import Flask

# Import routes
from .auth import bp as auth_bp
from .energy import bp as energy_bp


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.db'),
        OLD_DATABASE=os.path.join(
            app.instance_path, 'modbusData.db')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize db
    from .core import db
    db.init_app(app)

    # Register routes
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(energy.bp, url_prefix='/energy')

    @app.route('/')
    def test():
        return 'Hello world'

    return app
