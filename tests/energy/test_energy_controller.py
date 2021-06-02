import pytest
from app.energy.controller import EnergyController

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