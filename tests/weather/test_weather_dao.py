from app.weather.dao import WeatherDAO
from app.weather.domain import WeatherPoint
from app.core.db import get_db, init_db

def test_insertWeatherData(app):
    # Arrange
    sql_query = 'SELECT COUNT(date) FROM weather'
    weatherPoint = WeatherPoint('2021-04-20 22:45:14', 6.73, 100, 1.95, 1023)
    with app.app_context():
        init_db()  # Empty the database before running this tests.
    weatherDAO = WeatherDAO()

    # Act
    with app.app_context():
        weatherDAO.insertWeatherData(weatherPoint)
        db = get_db()
        count = db.execute(sql_query).fetchone()[0] # Get inserted data

    # Assert
    assert count > 0


def test_getWeatherData(app):
    # Arrange
    weatherDAO = WeatherDAO()

    # # Act
    with app.app_context():
        data = weatherDAO.getWeatherData()

    # Assert
    assert len(data) > 0