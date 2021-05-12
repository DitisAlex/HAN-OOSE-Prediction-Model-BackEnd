from app.weather.dao import WeatherDAO

class WeatherController:
    def __init__(self):
        self.weatherDAO = WeatherDAO()
        pass

    def insertWeather(self):
        self.weatherDAO.insertWeatherData()

    def getWeather(self):
        data = self.weatherDAO.getWeatherData()

        return data
