from app.core.db import get_db, get_rpi_db
from datetime import date, datetime, timedelta, timezone


class EnergyDAO:
    def __init__(self):
        pass

    def fetchProductionData(self):
        table = 'energy_production'
        fetch_query = 'SELECT Time, P1 FROM %s' % table

        db = get_db()
        cursor = db.cursor()
        # TODO: only fetch new data instead of everything
        cursor.execute(fetch_query)
        rows = cursor.fetchall()
        data = []

        currentDate = date.today()
        formattedDate = datetime.strptime(currentDate, "%Y-%m-%d %H:%M")
        currentDate_hours = formattedDate + timedelta(hours=-4)
        currentDate_hoursFormat = currentDate_hours.strftime('%Y-%m-%d %H:%M')

        for row in rows:
            productionDate = row[0]
            productionDateFormat = datetime.fromtimestamp(productionDate)
            productionDate_hours = productionDateFormat + timedelta(hours=2)
            productionDate_hoursFormat = productionDate_hours.strftime(
                '%Y-%m-%d %H:%M')

            if(productionDate_hoursFormat > currentDate_hoursFormat):
                englishFormat = productionDate_hours.strftime('%I:%M %p')

                data.append({
                    'labels': englishFormat,
                    'values': row[1]
                })
        return data

    def fetchData(self, type):
        table = 'Grid' if type == 'consumption' else 'PV'
        fetch_query = 'SELECT * FROM %s' % table

        db = get_rpi_db()
        cursor = db.cursor()
        # TODO: only fetch new data instead of everything
        cursor.execute(fetch_query)
        rows = cursor.fetchall()

        data = []
        for row in rows:
            data.append(list(row))

        return data

    def insertData(self, type, data):
        table = 'energy_consumption' if type == 'consumption' else 'energy_production'
        insert_query = 'INSERT INTO %s VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)' % table

        db = get_db()
        cursor = db.cursor()

        for row in data:
            var = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                   row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20])
            cursor.execute(insert_query, var)

        return ''
