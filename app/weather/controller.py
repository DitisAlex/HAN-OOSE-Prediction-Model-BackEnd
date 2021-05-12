from app.core.db import get_db, close_db

from datetime import datetime, timedelta, timezone
from pandas import pandas as pd
import numpy as np
from pyowm.utils import timestamps
from pyowm.owm import OWM


class WeatherController:
    def __init__(self):
        pass

    def getWeatherData(self):
        # Setup weather
        owm = OWM('1a4df9d4817c3d16e92b272d59531753')
        mgr = owm.weather_manager()
        one_call = mgr.one_call(lat=51, lon=5)
        forecast_hourly = one_call.forecast_hourly
        forecast_hourly[0].temperature('celsius')['temp']

        nr_of_weathers = len(forecast_hourly)
        Cloud = np.zeros(len(forecast_hourly))
        Temperature = np.zeros(len(forecast_hourly))
        Wind = np.zeros(len(forecast_hourly))
        Press = np.zeros(len(forecast_hourly))

        # Open database
        db = get_db()
        cur = db.cursor()

        for i in range(nr_of_weathers):
            dt = (datetime.fromtimestamp(forecast_hourly[i].ref_time)).strftime(
                '%Y-%m-%d %H:%M:%S')

            cur.execute('''INSERT INTO weather VALUES (?,?,?,?,?)''', (
                        dt,
                        forecast_hourly[i].temperature('celsius')['temp'],
                        forecast_hourly[i].clouds,
                        forecast_hourly[i].wind()['speed'],
                        forecast_hourly[i].pressure['press']))

        close_db(db)

        return ""
