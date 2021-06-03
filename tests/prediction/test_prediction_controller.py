from app.prediction.controller import PredictionController
from app.core.db import get_db
import pandas as pd

# def test_getProductionPrediction(monkeypatch):
#     # Arrange

#     hours = 3

#     # Mock dao functions.
#     class Recorder(object):
#         called1 = False
#         called2 = False
#         called3 = False

#     def fake_getDataForPrediction(self): # This isn't great but since the function we got from Kaggle uses the raw result of the SQL query, this is the only way we can supply dummy data.
#         Recorder.called1 = True

#         db = get_db()
#         query = '''SELECT * FROM energy_production ORDER BY time DESC LIMIT 24'''
#         data = pd.read_sql_query(query, db)

#         return data

#     def fake_deleteNewerPredictions(self, currentTime):
#         Recorder.called2 = True

#     def fake_insertPrediction(self, predictionPoint):
#         Recorder.called3 = True

#     monkeypatch.setattr(
#         'app.energy.dao.EnergyDAO.getDataForPrediction', fake_getDataForPrediction)

#     monkeypatch.setattr(
#         'app.prediction.dao.PredictionDAO.deleteNewerPredictions', fake_deleteNewerPredictions)
        
#     monkeypatch.setattr(
#         'app.prediction.dao.PredictionDAO.insertPrediction', fake_insertPrediction)

#     # Act
#     predictionController = PredictionController()
#     result = predictionController.getProductionPrediction(hours)
    

#     # Assert
#     assert len(result) == hours
#     assert Recorder.called1
#     assert Recorder.called2
#     assert Recorder.called3

def test_getProductionPredictionNoPVData(monkeypatch):
    # Arrange

    hours = 3


    # Mock dao functions.
    class Recorder(object):
        called1 = False
        called2 = False
        called3 = False

    def fake_getDataForPrediction(self):
        Recorder.called1 = True
        return []

    def fake_deleteNewerPredictions(self, currentTime):
        Recorder.called2 = True

    def fake_insertPrediction(self, predictionPoint):
        Recorder.called3 = True

    monkeypatch.setattr(
        'app.energy.dao.EnergyDAO.getDataForPrediction', fake_getDataForPrediction)

    monkeypatch.setattr(
        'app.prediction.dao.PredictionDAO.deleteNewerPredictions', fake_deleteNewerPredictions)
        
    monkeypatch.setattr(
        'app.prediction.dao.PredictionDAO.insertPrediction', fake_insertPrediction)


    # Act
    predictionController = PredictionController()
    result = predictionController.getProductionPrediction(hours)
    

    # Assert
    assert Recorder.called1
    assert not Recorder.called2
    assert not Recorder.called3
    assert len(result) == 0
