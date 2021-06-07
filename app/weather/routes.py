from app.weather import bp
from app.weather.controller import WeatherController

@bp.route('', methods=['POST'])
def insertWeatherData():

    try:
        c = WeatherController()
        c.insertWeatherData()
        return "Weather data inserted"
    except BaseException as e:
        return "Weather data not inserted: " +  e