import pytest
from datetime import datetime, timedelta
from app.prediction.controller import PredictionController
from app.core.db import get_db
import pandas as pd


def test_getProductionPrediction(app, monkeypatch):
    # Arrange
    hours=1
    mock_result_makePrediction = [[5000], [6000], [3000], [4000]]  # Hardcoded
    expected_result = (datetime.now() + timedelta(hours=2)).strftime('%H:%M:%S') + \
        ' ' + (datetime.now() + timedelta(hours=2+1)
               ).strftime('%H:%M:%S') + ' ' + str(mock_result_makePrediction[0][0])

    # Mock functions

    class Recorder(object):
        called1 = False
        called2 = False
        called3 = False
        called4 = False

    # This isn't great but since the function we got from Kaggle uses the raw result of the SQL query, this is the only way we can supply dummy data.
    def fake_loadModel(self):
        Recorder.called1 = True

    def fake_makePrediction(self, hours):
        Recorder.called2 = True
        return mock_result_makePrediction

    def fake_deleteNewerPredictions(self, currentTime):
        Recorder.called3 = True

    def fake_insertPrediction(self, predictionPoint):
        Recorder.called4 = True

    monkeypatch.setattr(
        'app.prediction.controller.PredictionController.loadModel', fake_loadModel)

    monkeypatch.setattr(
        'app.prediction.controller.PredictionController.makePrediction', fake_makePrediction)

    monkeypatch.setattr(
        'app.prediction.dao.PredictionDAO.deleteNewerPredictions', fake_deleteNewerPredictions)

    monkeypatch.setattr(
        'app.prediction.dao.PredictionDAO.insertPrediction', fake_insertPrediction)

    # Act
    with app.app_context():
        pc = PredictionController()
        result = pc.getProductionPrediction(hours)

    # Assert
    assert len(result) == hours
    assert Recorder.called1
    assert Recorder.called2
    assert Recorder.called3
    assert Recorder.called4
    assert expected_result == str(result[0])


def test_getProductionPredictionNoPVData(app, monkeypatch):
    # Arrange
    hours = 1
    mock_result_makePrediction = []
    expected_result = []

    # Mock functions

    class Recorder(object):
        called1 = False
        called2 = False
        called3 = False
        called4 = False

    # This isn't great but since the function we got from Kaggle uses the raw result of the SQL query, this is the only way we can supply dummy data.
    def fake_loadModel(self):
        Recorder.called1 = True

    def fake_makePrediction(self, hours):
        Recorder.called2 = True
        return mock_result_makePrediction

    def fake_deleteNewerPredictions(self, currentTime):
        Recorder.called3 = True

    def fake_insertPrediction(self, predictionPoint):
        Recorder.called4 = True

    monkeypatch.setattr(
        'app.prediction.controller.PredictionController.loadModel', fake_loadModel)

    monkeypatch.setattr(
        'app.prediction.controller.PredictionController.makePrediction', fake_makePrediction)

    monkeypatch.setattr(
        'app.prediction.dao.PredictionDAO.deleteNewerPredictions', fake_deleteNewerPredictions)

    monkeypatch.setattr(
        'app.prediction.dao.PredictionDAO.insertPrediction', fake_insertPrediction)

    # Act
    with app.app_context():
        pc = PredictionController()
        result = pc.getProductionPrediction(hours)

    # Assert
    assert result == expected_result
    assert Recorder.called1
    assert Recorder.called2
    assert not Recorder.called3
    assert not Recorder.called4
