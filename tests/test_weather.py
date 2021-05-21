import pytest
from app.core.db import get_db, init_db

def test_getWeatherDataWithEmptyDatabase(client, app):
  #Arrange
  with app.app_context():
    init_db() # Empty the database before running this tests.

  # Act
  response = client.get('/weather')
  
  # Assert
  assert response.status_code == 204

def test_insertWeatherData(client, app):
  # Arrange
  sql_query = 'SELECT COUNT(date) FROM weather'
  with app.app_context():
    init_db() # Empty the database before running this tests.

  # Act
  response = client.get('/weather/fetch')
  with app.app_context():
    db = get_db()
    count = db.execute(sql_query).fetchone()[0]

  # Assert
  assert response.status_code == 200
  assert count > 0

def test_getWeatherData(client, app):
  #Arrange

  # Act
  response = client.get('/weather')
  # with app.app_context():
  weatherArray = response.get_json()
  
  # Assert
  assert response.status_code == 200
  assert len(weatherArray) > 0
  assert len(weatherArray[0]) == 5
  