import os
import tempfile

import pytest

from app import create_app
from app.core.db import get_db, init_db

# read in SQL for populating test data
with current_app.open_resource(("test-data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


# Create and configure new app instance for each test
@pytest.fixture
def app():
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()

    # create the app with common test config and set database to temporary file
    app = create_app({"TESTING": True, "DATABASE": db_path})

    # create the database and load test data
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)

# Test client for the app
@pytest.fixture
def client(app):
    return app.test_client()

# Test runner for app's Click commands
@pytest.fixture
def runner(app):
    return app.test_cli_runner()
