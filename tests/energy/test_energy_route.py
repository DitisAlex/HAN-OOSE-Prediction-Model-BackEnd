def test_fetchConsumptionData(client, monkeypatch):
    # Arrange
    # Mock controller function.
    class Recorder(object):
        called = False

    def fake_fetchEnergyData(self, type):
        Recorder.called = True

    monkeypatch.setattr(
        'app.energy.controller.EnergyController.fetchEnergyData', fake_fetchEnergyData)

    # Act
    response = client.post('/energy/consumption/fetch')

    # Assert
    assert response.status_code == 200
    assert b'Successfully' in response.data
    assert Recorder.called


def test_fetchEnergyData(client, monkeypatch):
    # Arrange
    # Mock controller function.
    class Recorder(object):
        called = False

    def fake_fetchEnergyData(self, type):
        Recorder.called = True

    monkeypatch.setattr(
        'app.energy.controller.EnergyController.fetchEnergyData', fake_fetchEnergyData)

    # Act
    response = client.post('/energy/production/fetch')

    # Assert
    assert response.status_code == 200
    assert b'Successfully' in response.data
    assert Recorder.called

def test_getProductionData(client, monkeypatch):
    # Arrange
    # Mock controller function.
    class Recorder(object):
        called = False

    def fake_getProductionData(self, type):
        Recorder.called = True

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

    monkeypatch.setattr(
        'app.energy.controller.EnergyController.getEnergyData', fake_getConsumptionData)

    # Act
    response = client.get('/energy/consumption')

    # Assert
    assert response.status_code == 200
    assert Recorder.called