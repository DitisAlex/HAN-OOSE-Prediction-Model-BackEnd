import pytest
from app.core.db import get_db, init_db

def test_fetchConsumptionData(client, app):
  # Arrange
  sql_query = 'SELECT COUNT(no) FROM energy_consumption'
  with app.app_context():
    init_db() # Empty the database before running this tests.

  # Act
  response = client.post('/energy/consumption/fetch')
  with app.app_context():
    db = get_db()
    count = db.execute(sql_query).fetchone()[0]
    print('\nTEST\n')
    print(count)
  
  # Assert
  assert response.status_code == 200
  assert count > 1

def test_fetchProductionData(client, app):
  # Arrange
  sql_query = 'SELECT COUNT(no) FROM energy_production'
  with app.app_context():
    init_db() # Empty the database before running this tests.

  # Act
  response = client.post('/energy/production/fetch')
  with app.app_context():
    db = get_db()
    count = db.execute(sql_query).fetchone()[0]
    print('\nTEST\n')
    print(count)
  
  # Assert
  assert response.status_code == 200
  assert count > 1

# def test_getConsumptionData(client, app):
#   #Arrange

#   # Act
#   response = client.get('/consumption')
#   weatherArray = response.get_json()
  
#   # Assert
#   assert response.status_code == 200
#   assert len(weatherArray) > 0
#   assert len(weatherArray[0]) == 5

# def test_getProductionData(client, app):
#   #Arrange

#   # Act
#   response = client.get('/production')
#   weatherArray = response.get_json()
  
#   # Assert
#   assert response.status_code == 200
#   assert len(weatherArray) > 0
#   assert len(weatherArray[0]) == 5