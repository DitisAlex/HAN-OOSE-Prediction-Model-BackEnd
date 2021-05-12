from flask import request, abort
from app.weather import bp
from app.weather.controller import WeatherController

from flask import jsonify


@bp.route('', methods=['POST'])
def insertWeatherData():
    c = WeatherController()

    try:
        c.insertWeather()

        return "Weather data inserted"
    except KeyError:  # KeyError = missing key in json
        abort(401, "Invalid data")

@bp.route('', methods=['GET'])
def getWeather():
    c = WeatherController()

    try:
        result = c.getWeather()

        return result
    except KeyError:  # KeyError = missing key in json
        abort(401, "Invalid data")