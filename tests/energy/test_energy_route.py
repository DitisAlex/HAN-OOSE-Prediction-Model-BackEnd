def test_getProductionData(client, monkeypatch):
    # Arrange
    # Mock controller function.
    class Recorder(object):
        called = False

    def fake_getProductionData(self, type):
        Recorder.called = True
        return [1, 2]

    monkeypatch.setattr(
        'app.energy.controller.EnergyController.getEnergyData', fake_getProductionData)

    # Act
    response = client.get('/energy/production')

    # Assert
    assert response.status_code == 200
    assert Recorder.called

def test_getConsumptionData(client, monkeypatch):
    # Arrange
    # Mock controller function.

    class Recorder(object):
        called = False

    def fake_getConsumptionData(self, type):
        Recorder.called = True
        return [1, 2]

    monkeypatch.setattr(
        'app.energy.controller.EnergyController.getEnergyData', fake_getConsumptionData)

    # Act
    response = client.get('/energy/consumption')

    # Assert
    assert response.status_code == 200
    assert Recorder.called