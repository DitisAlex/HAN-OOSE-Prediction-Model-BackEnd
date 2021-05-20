from app.weather.dao import WeatherDAO
from pyowm.owm import OWM

class PredictionController:
    def __init__(self):
        self.weatherDAO = WeatherDAO()
        pass

    def getProductionPrediction(self, hours):
        predictionData = []

        dummyData = [10, 4, 18, 12]

        for i in range(hours):
            predictionData.append(dummyData[i])

        return predictionData
