from app.energy.controller import EnergyController


def test_fetchConsumptionData(monkeypatch):
    # Arrange
    # Mock dao functions.
    class Recorder(object):
        called1 = False
        called2 = False

    def fake_fetchData(self, type):
        Recorder.called1 = True

    def fake_insertData(self, type, data):
        Recorder.called2 = True

    monkeypatch.setattr(
        'app.energy.dao.EnergyDAO.fetchData', fake_fetchData)

    monkeypatch.setattr(
        'app.energy.dao.EnergyDAO.insertData', fake_insertData)

    # Act
    energyController = EnergyController()
    energyController.fetchConsumptionData()

    # Assert
    assert Recorder.called1
    assert Recorder.called2

def test_fetchProductionData(monkeypatch):
    # Arrange
    # Mock dao functions.
    class Recorder(object):
        called1 = False
        called2 = False

    def fake_fetchData(self, type):
        Recorder.called1 = True

    def fake_insertData(self, type, data):
        Recorder.called2 = True

    monkeypatch.setattr(
        'app.energy.dao.EnergyDAO.fetchData', fake_fetchData)

    monkeypatch.setattr(
        'app.energy.dao.EnergyDAO.insertData', fake_insertData)

    # Act
    energyController = EnergyController()
    energyController.fetchProductionData()

    # Assert
    assert Recorder.called1
    assert Recorder.called2
