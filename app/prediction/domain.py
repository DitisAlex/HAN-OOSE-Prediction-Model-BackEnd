class PredictionPoint:
    def __init__(self, predictedOn, predictedDate, prediction):
        self.__predictedOn = predictedOn
        self.__predictedDate = predictedDate
        self.__prediction = prediction
    
    def getPredictedOn(self):
        return self.__predictedOn
    
    def getPredictedDate(self):
        return self.__predictedDate
    
    def getPrediction(self):
        return self.__prediction
