from app.core.db import get_db, get_rpi_db
from datetime import datetime, timedelta, timezone
import numpy as np
from pyowm.owm import OWM
from flask import jsonify

class WeatherDAO:
  def __init__(self):
    pass

  def insertWeatherData(self):

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

  def getWeatherData(self):   
      
      data = []
      db = get_db()
      cur = db.cursor()
      cur.execute("SELECT * FROM Weather LIMIT 24") # get last 24 hours

      rows = cur.fetchall()

      data = []
      
      for row in rows:
          data.append([x for x in row])

      return jsonify(data)
