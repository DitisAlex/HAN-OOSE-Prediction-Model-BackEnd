from app import energy
from app.core.db import get_db, get_rpi_db
from datetime import datetime, timedelta
import pandas as pd
from app.energy.domain import EnergyPoint


class EnergyDAO:
    def getEnergyData(self, type):

        DATETIME_FORMAT = '%Y-%m-%d %H:%M'

        table = 'energy_consumption' if type == 'consumption' else 'energy_production'
        fetch_query = 'SELECT * FROM %s' % table

        db = get_db()
        cursor = db.cursor()
        cursor.execute(fetch_query)
        rows = cursor.fetchall()

        energyPoints = []
        if len(rows) == 0:
            return []
        else:
            for row in rows:
                energyPoint = [x for x in row]
                energyPoints.append(
                    EnergyPoint(energyPoint[0], energyPoint[1], energyPoint[2], energyPoint[3], energyPoint[4], energyPoint[5], energyPoint[6],
                                energyPoint[7], energyPoint[8], energyPoint[9], energyPoint[
                                    10], energyPoint[11], energyPoint[12], energyPoint[13],
                                energyPoint[14], energyPoint[15], energyPoint[16], energyPoint[17], energyPoint[18], energyPoint[19], energyPoint[20])
                )

        currentDate = datetime.today()
        currentDateFormat = currentDate.strftime(DATETIME_FORMAT)
        currentDate_hours = currentDate + timedelta(hours=-24)
        currentDate_hoursFormat = currentDate_hours.strftime(DATETIME_FORMAT)

        energyData = []
        if len(energyPoints) == 0:
            return []
        else:
            for i in range(len(energyPoints)):
                energyDate = energyPoints[i].getTime()
                energyDateTimestamp = datetime.fromtimestamp(energyDate)
                twentyfourHourFormat = energyDateTimestamp.strftime(DATETIME_FORMAT)

                if(twentyfourHourFormat > currentDate_hoursFormat and twentyfourHourFormat < currentDateFormat):
                    twelveHourTime = energyDateTimestamp.strftime('%I:%M %p')

                    energyData.append({
                        'labels': twelveHourTime,
                        'datetime': twentyfourHourFormat,
                        'values': energyPoints[i].getP1()
                    })

            if len(energyData) > 0:
                return energyData
            else:
                print("TEST")

                return []

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

        cursor.execute("SELECT no FROM %s" % table)
        rows = cursor.fetchall()

        existing_ids = []
        for row in rows:
            existing_ids.append(list(row)[0])

        for row in data:
            if(row[0] not in existing_ids):
                var = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                       row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20])
                cursor.execute(insert_query, var)

        return ''

    def getDataForPrediction(self):

        db = get_db()

        query = '''SELECT * FROM energy_production ORDER BY time DESC LIMIT 24'''

        data = pd.read_sql_query(query, db)

        return data
