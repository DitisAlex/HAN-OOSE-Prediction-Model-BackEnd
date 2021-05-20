import pytest
from app.energy.dao import EnergyDAO
from app.core.db import get_db, init_db


@pytest.mark.parametrize(
    'type',
    [
        ('consumption'), 
        ('production')
    ]
)
def test_fetch_data(app, type):
    # Arrange
    with app.app_context():
        init_db()  # Empty the database before running this tests.

    # # Act
    energyDAO = EnergyDAO()
    with app.app_context():
        data = energyDAO.fetchData(type)

    # Assert
    assert len(data) > 0

@pytest.mark.parametrize(
    'type',
    [
        ('consumption'), 
        ('production')
    ]
)
def test_insert_data(app, type):
    # Arrange
    table = 'energy_consumption' if type == 'consumption' else 'energy_production'
    sql_query = 'SELECT COUNT(no) FROM %s'%table
    dummy_data = [[1, 1617589961, 234.5, 234.2, 234.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 50.0]]
    with app.app_context():
        init_db()  # Empty the database before running this tests.

    # Act
    energyDAO = EnergyDAO()
    with app.app_context():
        energyDAO.insertData(type, dummy_data)
        db = get_db()
        count = db.execute(sql_query).fetchone()[0] # Get inserted data

    # Assert
    assert count > 0
