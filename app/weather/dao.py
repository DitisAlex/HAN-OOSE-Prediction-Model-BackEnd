from app.core.db import get_db, get_rpi_db
from app.weather.domain import WeatherPoint
from datetime import datetime, timedelta, timezone
from flask import jsonify

class WeatherDAO:
  def __init__(self):
    pass

  def insertWeatherData(self, forecast_hourly):

    # Open database
    db = get_db()
    cur = db.cursor()

    for i in range(len(forecast_hourly)):
        dt = (datetime.fromtimestamp(forecast_hourly[i].ref_time)).strftime('%Y-%m-%d %H:%M:%S')
        query = '''INSERT INTO weather VALUES (?,?,?,?,?)'''
        values = (
                    dt,
                    forecast_hourly[i].temperature('celsius')['temp'],
                    forecast_hourly[i].clouds,
                    forecast_hourly[i].wind()['speed'],
                    forecast_hourly[i].pressure['press'])

        cur.execute(query, values)

  def getWeatherData(self):   
    
      db = get_db()
      cur = db.cursor()
      query = "SELECT * FROM Weather LIMIT 24" # get last 24 hours
      cur.execute(query) 

      rows = cur.fetchall()

      data = []
      
      for row in rows:
        weatherPoint = [x for x in row]
        data.append(WeatherPoint(weatherPoint[0], weatherPoint[1], weatherPoint[2], weatherPoint[3], weatherPoint[4]))

      return data
