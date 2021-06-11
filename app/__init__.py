import os

from flask import Flask
from .tasks import scheduler

# Import routes
from .energy import bp as energy_bp
from .weather import bp as weather_bp
from .prediction import bp as prediction_bp

from app.energy import EnergyController


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        DEBUG=True,
        DATABASE=os.path.join(app.instance_path, 'database.db'),
        RPI_DATABASE=os.path.join(
            app.instance_path, 'modbusData.db')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Check if instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize db
    from .core import db
    db.init_app(app)      

    # Initialize task scheduler
    if (not app.config['TESTING']):
        scheduler.init_app(app)

        with app.app_context():
            # init table data
            # initial_fetch()

            if is_debug_mode() and not is_werkzeug_reloader_process() and not app.config['TESTING']:
                pass
            else:
                from .tasks import tasks
                # scheduler.start()

            from .tasks import events

    # Register routes
    app.register_blueprint(energy_bp, url_prefix='/energy')
    app.register_blueprint(weather_bp, url_prefix='/weather')
    app.register_blueprint(prediction_bp, url_prefix='/prediction')

    return app

# Helper functions


def is_debug_mode():
    """Get app debug status."""
    debug = os.environ.get("FLASK_DEBUG")
    if not debug:
        return os.environ.get("FLASK_ENV") == "development"
    return debug.lower() not in ("0", "false", "no")


def is_werkzeug_reloader_process():
    """Get werkzeug status."""
    return os.environ.get("WERKZEUG_RUN_MAIN") == "true"

def initial_fetch():
    ec = EnergyController()
    ec.fetchEnergyData("production")
    ec.fetchEnergyData("consumption")
