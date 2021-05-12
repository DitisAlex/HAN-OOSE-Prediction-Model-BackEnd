from app.weather.dao import WeatherDAO
from pyowm.owm import OWM

class WeatherController:
    def __init__(self):
        self.weatherDAO = WeatherDAO()
        pass

    def insertWeather(self):

        # Setup weather, taken from Pytorch model.
        owm = OWM('1a4df9d4817c3d16e92b272d59531753')
        mgr = owm.weather_manager()
        one_call = mgr.one_call(lat=51, lon=5)
        forecast_hourly = one_call.forecast_hourly
        forecast_hourly[0].temperature('celsius')['temp']

        self.weatherDAO.insertWeatherData(forecast_hourly)

    def getWeather(self):
        weatherData = self.weatherDAO.getWeatherData()

        return weatherData.data
