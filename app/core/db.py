import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from pandas import pandas as pd


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,timeout=10
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def get_rpi_db():
    #TODO: Pull data from Raspberry Pi! For now we mock this using modbusData.db...

    if 'rpi_db' not in g:
        g.rpi_db = sqlite3.connect(
            current_app.config['RPI_DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.rpi_db.row_factory = sqlite3.Row

    return g.rpi_db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.commit()
        db.close()

def close_rpi_db(e=None):
    db = g.pop('rpi_db', None)

    if db is not None:
        db.commit()
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# Clear existing data and create new empty tables.
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.') 

# Insert test data into db.
@click.command('insert-test-data')
@with_appcontext
def insert_test_data_command():
    db = get_db()

    with current_app.open_resource("dummy-data.sql", "rb") as f:
        db.executescript(f.read().decode("utf8"))
    
    click.echo('Inserted test data.')

@click.command('show-table')
@click.argument('table')
@with_appcontext
def show_db_command(table):
    """Get tables."""
    db = get_db()
    query = "SELECT * FROM %s;"%table
    df = pd.read_sql_query(query, db)

    print(df)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.teardown_appcontext(close_rpi_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(insert_test_data_command)
    app.cli.add_command(show_db_command)
