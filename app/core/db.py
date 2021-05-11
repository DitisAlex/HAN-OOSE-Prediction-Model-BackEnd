import sqlite3
import os;
import click
from flask import current_app, g
from flask.cli import with_appcontext
from pandas import pandas as pd

# Connect to the application's configured database. 
# The connection is unique for each request and will be reused if this is called again.
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def get_old_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            # Dit is niet nodig. je kunt de database replace met de volgende code:
            # app = create_app({"TESTING": True, "DATABASE": db_path}) gr ilias
            current_app.config['OLD_DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.commit()
        db.close()

# Clear existing data and create new tables.
@click.command('init-db')
@with_appcontext
def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql", "rb") as f:
        db.executescript(f.read().decode("utf8"))

# Insert test data into db.
@click.command('insert-test-data')
@with_appcontext
def insert_test_data():
    db = get_db()

    with current_app.open_resource("test-data.sql", "rb") as f:
        db.executescript(f.read().decode("utf8"))

# Register database functions with the Flask app. This is called by the application factory
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db)
    app.cli.add_command(insert_test_data)
