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

    def __str__(self):
        return self.__predictedOn.strftime("%H:%M:%S") + ' ' + self.__predictedDate.strftime("%H:%M:%S") + ' ' + str(self.__prediction)
