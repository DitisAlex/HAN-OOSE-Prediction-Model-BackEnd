from flask import jsonify
from app.weather import bp
from app.weather.controller import WeatherController

from flask import jsonify


@bp.route('', methods=['POST'])
def insertWeatherData():

    try:
        c = WeatherController()
        c.insertWeatherData()
        return "Weather data inserted"
    except TypeError:
        return "Weather data not inserted: required arguments missing"
    except AttributeError:
        return "Weather data not inserted: no data found"

    # except:
    #     return "Weather data not inserted"