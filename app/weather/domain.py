class WeatherPoint:
    def __init__(self, date, temperature, cloud, wind, pressure):
        self.__date = date
        self.__temperature = temperature
        self.__cloud = cloud
        self.__wind = wind
        self.__pressure = pressure
    
    def getDate(self):
        return self.__date

    def setDate(self, date):
        self.__date = date
    
    def getTemperature(self):
        return self.__temperature

    def setTemperature(self, temperature):
        self.__temperature = temperature
    
    def getCloud(self):
        return self.__cloud

    def setCloud(self, cloud):
        self.__cloud = cloud
    
    def getWind(self):
        return self.__wind

    def setWind(self, wind):
        self.__wind = wind
    
    def getPressure(self):
        return self.__pressure

    def setPressure(self, pressure):
        self.__pressure = pressure
