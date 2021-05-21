from app.prediction.controller import PredictionController

def test_getProductionPrediction(monkeypatch):
    # Arrange

    hours = 3

    # Mock dao functions.
    class Recorder(object):
        called1 = False
        called2 = False

    def fake_deleteNewerPredictions(self, currentTime):
        Recorder.called1 = True

    def fake_insertPrediction(self, predictionPoint):
        Recorder.called2 = True

    monkeypatch.setattr(
        'app.prediction.dao.PredictionDAO.deleteNewerPredictions', fake_deleteNewerPredictions)
        
    monkeypatch.setattr(
        'app.prediction.dao.PredictionDAO.insertPrediction', fake_insertPrediction)


    # Act
    predictionController = PredictionController()
    result = predictionController.getProductionPrediction(hours)
    

    # Assert
    assert len(result) == hours
    assert Recorder.called1
    assert Recorder.called2
