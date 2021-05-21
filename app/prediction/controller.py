from app.prediction.dao import PredictionDAO
from app.prediction.domain import PredictionPoint
from datetime import datetime, timedelta

class PredictionController:
    def __init__(self):
        self.predictionDAO = PredictionDAO()
        pass

    def getProductionPrediction(self, hours):
        predictionData = []

        dummyPredictions = [10, 4, 18, 12] # standin until real predictions are generated

        currentTime = datetime.now()

        self.predictionDAO.deleteNewerPredictions(currentTime) # if there are predictions with a time that this prediction will also predict, delete them

        for i in range(hours):

            predictionTime = currentTime + timedelta(hours=i)
            
            predictionPoint = PredictionPoint(currentTime, predictionTime, dummyPredictions[i])

            self.predictionDAO.insertPrediction(predictionPoint)

            predictionData.append(dummyPredictions[i])

        return predictionData
