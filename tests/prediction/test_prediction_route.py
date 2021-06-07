from app.prediction.domain import PredictionPoint
from flask import jsonify
from datetime import datetime, timedelta, timezone

GETPRODUCTIONPREDICTION_PATH = 'app.prediction.controller.PredictionController.getProductionPrediction'

def test_getPredictionSuccesfully(client, monkeypatch):
    # Arrange
    # Mock controller function.
    class Recorder(object):
        called = False

    def fake_ProductionPrediction(self, hours):
        Recorder.called = True

        currentTime = datetime.now() + timedelta(hours=2)

        predictionData = []

        for i in range(hours):

            predictionTime = currentTime + timedelta(hours=i+1)
            
            predictionPoint = PredictionPoint(currentTime, predictionTime, 327.35+i)

            predictionData.append(predictionPoint)

        
        return predictionData


    monkeypatch.setattr(GETPRODUCTIONPREDICTION_PATH, fake_ProductionPrediction)

    # Act
    response = client.get('/prediction/3')

    # Assert
    assert response.status_code == 200
    assert b'"value": 327.35' in response.data
    assert b'"value": 328.35' in response.data
    assert b'"value": 329.35' in response.data
    assert b'"value": 330.35' not in response.data
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
    assert response.status_code == 404
    assert Recorder.called == False

def test_getPredictionNoPVData(client, monkeypatch):
    # Arrange
    # Mock controller function.
    class Recorder(object):
        called = False

    def fake_ProductionPrediction(self, hours):
        Recorder.called = True
        return []


    monkeypatch.setattr(GETPRODUCTIONPREDICTION_PATH, fake_ProductionPrediction)

    # Act
    response = client.get('/prediction/2')

    # Assert
    assert response.status_code == 404
    assert b'Not enough historical data' in response.data
    assert Recorder.called == True

def test_getPredictionHoursOutOfBounds(client, monkeypatch):
    # Arrange
    # Mock controller function.
    class Recorder(object):
        called = False

    def fake_ProductionPrediction(self, hours):
        Recorder.called = True


    monkeypatch.setattr(GETPRODUCTIONPREDICTION_PATH, fake_ProductionPrediction)

    # Act
    response = client.get('/prediction/5')

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


    monkeypatch.setattr(GETPRODUCTIONPREDICTION_PATH, fake_ProductionPrediction)

    # Act
    response = client.get('/prediction/viktorgreat')

    # Assert
    assert response.status_code == 400
    assert b'supplied value was not an integer' in response.data
    assert Recorder.called == False
