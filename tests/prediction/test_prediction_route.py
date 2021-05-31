def test_getPredictionSuccesfully(client, monkeypatch):
    # Arrange
    # Mock controller function.
    class Recorder(object):
        called = False

    def fake_ProductionPrediction(self, hours):
        Recorder.called = True
        data = []
        for i in range(hours):
            data.append(327)
        return data


    monkeypatch.setattr(
        'app.prediction.controller.PredictionController.getProductionPrediction', fake_ProductionPrediction)

    # Act
    response = client.get('/prediction?hours=3')

    # Assert
    assert response.status_code == 200
    assert b'[327,327,327]' in response.data
    assert Recorder.called

def test_getPredictionNoHours(client, monkeypatch):
    # Arrange
    # Mock controller function.
    class Recorder(object):
        called = False

    def fake_ProductionPrediction(self, hours):
        Recorder.called = True


    monkeypatch.setattr(
        'app.prediction.controller.PredictionController.getProductionPrediction', fake_ProductionPrediction)

    # Act
    response = client.get('/prediction')

    # Assert
    assert response.status_code == 400
    assert b'Missing query parameter' in response.data
    assert Recorder.called == False

def test_getPredictionHoursOutOfBounds(client, monkeypatch):
    # Arrange
    # Mock controller function.
    class Recorder(object):
        called = False

    def fake_ProductionPrediction(self, hours):
        Recorder.called = True


    monkeypatch.setattr(
        'app.prediction.controller.PredictionController.getProductionPrediction', fake_ProductionPrediction)

    # Act
    response = client.get('/prediction?hours=5')

    # Assert
    assert response.status_code == 400
    assert b'needs a value from 1 to 4' in response.data
    assert Recorder.called == False

def test_getPredictionHoursNaN(client, monkeypatch):
    # Arrange
    # Mock controller function.
    class Recorder(object):
        called = False

    def fake_ProductionPrediction(self, hours):
        Recorder.called = True


    monkeypatch.setattr(
        'app.prediction.controller.PredictionController.getProductionPrediction', fake_ProductionPrediction)

    # Act
    response = client.get('/prediction?hours=viktorgreat')

    # Assert
    assert response.status_code == 400
    assert b'supplied value was not an integer' in response.data
    assert Recorder.called == False
