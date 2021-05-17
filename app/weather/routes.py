from flask import jsonify
from app.weather import bp
from app.weather.controller import WeatherController

from flask import jsonify


@bp.route('/fetch', methods=['GET'])
def insertWeatherData():
    c = WeatherController()
    c.insertWeatherData()

    return "Weather data inserted"

@bp.route('', methods=['GET'])
def getWeather():
    c = WeatherController()
    results = c.getWeatherData()

    weatherData = []

    for result in results:
        weatherPoint = []

        weatherPoint.append(result.getDate())
        weatherPoint.append(result.getTemperature())
        weatherPoint.append(result.getCloud())
        weatherPoint.append(result.getWind())
        weatherPoint.append(result.getPressure())

        weatherData.append(weatherPoint)

    return jsonify(weatherData)
