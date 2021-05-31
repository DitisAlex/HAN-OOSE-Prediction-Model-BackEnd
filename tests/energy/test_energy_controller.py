import pytest
from app.energy.controller import EnergyController

@pytest.mark.parametrize(
    'type',
    [
        ('consumption'), 
        ('production')
    ]
)
def test_fetchEnergyData(monkeypatch, type):
    # Arrange
    # Mock dao functions.
    class Recorder(object):
        called1 = False
        called2 = False

    def fake_fetchEnergyData(self, type):
        Recorder.called1 = True

    def fake_insertEnergyData(self, type, data):
        Recorder.called2 = True

    monkeypatch.setattr(
        'app.energy.dao.EnergyDAO.fetchEnergyData', fake_fetchEnergyData)

    monkeypatch.setattr(
        'app.energy.dao.EnergyDAO.insertEnergyData', fake_insertEnergyData)

    # Act
    energyController = EnergyController()
    energyController.fetchEnergyData(type)

    # Assert
    assert Recorder.called1
    assert Recorder.called2

@pytest.mark.parametrize(
    'type',
    [
        ('consumption'), 
        ('production')
    ]
)
def test_getEnergyData(monkeypatch, type):
    # Arrange
    # Mock dao functions.
    class Recorder(object):
        called = False

    def fake_getEnergyData(self, type):
        Recorder.called = True

    monkeypatch.setattr(
        'app.energy.dao.EnergyDAO.getEnergyData', fake_getEnergyData)

    # Act
    energyController = EnergyController()
    energyController.getEnergyData(type)

    # Assert
    assert Recorder.called