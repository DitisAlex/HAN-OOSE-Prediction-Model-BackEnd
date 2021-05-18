import sqlite3
import pytest
from app.core.db import get_db, get_rpi_db


def test_get_close_db(app):
    # Arrange

    # Act
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    # Assert
    assert 'closed' in str(e.value)

def test_get_close_rpi_db(app):
    # Arrange

    # Act
    with app.app_context():
        rpi_db = get_rpi_db()
        assert rpi_db is get_rpi_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        rpi_db.execute('SELECT 1')

    # Assert
    assert 'closed' in str(e.value)

def test_init_db_command(runner, monkeypatch):
    # Arrange
    ## Mock function
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('app.core.db.init_db', fake_init_db)

    # Act
    result = runner.invoke(args=['init-db'])

    # Assert
    assert 'Initialized' in result.output
    assert Recorder.called


def test_insert_test_data_command(runner, monkeypatch):
    # Arrange

    # Act
    result = runner.invoke(args=['insert-test-data'])

    # Assert
    assert 'Inserted' in result.output

def test_show_db_command(runner, monkeypatch):
    # Arrange

    # Act
    result = runner.invoke(args=['show-table', 'weather'])

    # Assert
    assert 'wind' in result.output
