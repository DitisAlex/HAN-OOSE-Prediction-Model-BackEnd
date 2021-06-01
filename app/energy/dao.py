from app.core.db import get_db, get_rpi_db
from datetime import date, datetime, timedelta, timezone
from flask import abort

class EnergyDAO:
    def __init__(self):
        pass

    def getEnergyData(self, type):
        table = 'energy_consumption' if type == 'consumption' else 'energy_production'
        fetch_query = 'SELECT time, P1 FROM %s' % table

        db = get_db()
        cursor = db.cursor()
        cursor.execute(fetch_query)
        rows = cursor.fetchall()

        currentDate = datetime.today()
        currentDateFormat = currentDate.strftime('%Y-%m-%d %H:%M')
        currentDate_hours = currentDate + timedelta(hours=-4)
        currentDate_hoursFormat = currentDate_hours.strftime('%Y-%m-%d %H:%M')

        data = []
        if len(rows)==0:
            abort(404, description = "No data found")
        else:
            for row in rows:
                energyDate = row[0]
                energyDateFormat = datetime.fromtimestamp(energyDate)
                energyDate_hours = energyDateFormat + timedelta(hours=2)
                energyDate_hoursFormat = energyDate_hours.strftime(
                    '%Y-%m-%d %H:%M')

                if(energyDate_hoursFormat > currentDate_hoursFormat and energyDate_hoursFormat < currentDateFormat):
                    twelveHourTime = energyDate_hours.strftime('%I:%M %p')

                    data.append({
                        'labels': twelveHourTime,
                        'datetime': energyDate_hoursFormat,
                        'values': row[1]
                    })
            if len(data)> 0:
                return data
            else:
                abort(404, description = "No datas found")

    def fetchEnergyData(self, type):
        table = 'Grid' if type == 'consumption' else 'PV'
        fetch_query = 'SELECT * FROM %s' % table

        db = get_rpi_db()
        cursor = db.cursor()
        cursor.execute(fetch_query)
        rows = cursor.fetchall()

        data = []
        for row in rows:
            data.append(list(row))

        return data

    def insertEnergyData(self, type, data):
        table = 'energy_consumption' if type == 'consumption' else 'energy_production'
        insert_query = 'INSERT INTO %s VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)' % table

        db = get_db()
        cursor = db.cursor()

        for row in data:
            var = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                   row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20])
            cursor.execute(insert_query, var)

        return ''
