from app.weather.dao import WeatherDAO
from app.weather.domain import WeatherPoint
from datetime import datetime, timedelta, timezone
from pyowm.owm import OWM

class WeatherController:
    def __init__(self):
        self.weatherDAO = WeatherDAO()
        pass

    def insertWeatherData(self):

        # Setup weather, taken from Pytorch model.
        owm = OWM('1a4df9d4817c3d16e92b272d59531753')
        mgr = owm.weather_manager()
        one_call = mgr.one_call(lat=51, lon=5)
        current = one_call.current
        current.temperature('celsius')['temp']

        weatherPoint = WeatherPoint(
                datetime.fromtimestamp(current.ref_time).strftime('%Y-%m-%d %H:%M:%S'),
                current.temperature('celsius')['temp'],
                current.clouds,
                current.wind()['speed'],
                current.pressure['press'])

        self.weatherDAO.insertWeatherData(weatherPoint)

    def getWeatherData(self):
        weatherData = self.weatherDAO.getWeatherData()

        return weatherData
