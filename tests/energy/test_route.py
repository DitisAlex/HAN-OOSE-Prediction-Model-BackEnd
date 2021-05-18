import pytest
from app.energy.controller import EnergyController

def test_fetchConsumptionData(client, monkeypatch):
  # Arrange
  ## Mock controller function.
  class Recorder(object):
        called = False

  def fake_fetchConsumptionData(self):
      Recorder.called = True

  monkeypatch.setattr('app.energy.controller.EnergyController.fetchConsumptionData', fake_fetchConsumptionData)


  # Act
  response = client.post('/energy/consumption/fetch')

  # Assert
  assert response.status_code == 200
  assert b'Successfully' in response.data
  assert Recorder.called

def test_fetchProductionData(client, monkeypatch):
  # Arrange
  ## Mock controller function.
  class Recorder(object):
        called = False

  def fake_fetchProductionData(self):
      Recorder.called = True

  monkeypatch.setattr('app.energy.controller.EnergyController.fetchProductionData', fake_fetchProductionData)


  # Act
  response = client.post('/energy/production/fetch')

  # Assert
  assert response.status_code == 200
  assert b'Successfully' in response.data
  assert Recorder.called
