from flask import request, abort
from app.weather import bp
from app.weather.controller import WeatherController

from flask import jsonify


@bp.route('', methods=['POST'])
def getWeather():
    c = WeatherController()

    try:
        c.getWeatherData()

        return "Weather data inserted"
    except KeyError:  # KeyError = missing key in json
        abort(401, "Invalid data")
