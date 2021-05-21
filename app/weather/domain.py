class WeatherPoint:
    def __init__(self, date, temperature, cloud, wind, pressure):
        self.__date = date
        self.__temperature = temperature
        self.__cloud = cloud
        self.__wind = wind
        self.__pressure = pressure
    
    def getDate(self):
        return self.__date
    
    def getTemperature(self):
        return self.__temperature
    
    def getCloud(self):
        return self.__cloud
    
    def getWind(self):
        return self.__wind
    
    def getPressure(self):
        return self.__pressure
