from app import energy
from datetime import datetime, timedelta
from flask import abort

class EnergyDAO:
    def __init__(self):
        pass

    def getEnergyData(self, energyData):
        currentDate = datetime.today()
        currentDateFormat = currentDate.strftime('%Y-%m-%d %H:%M')
        currentDate_hours = currentDate + timedelta(hours=-250)
        currentDate_hoursFormat = currentDate_hours.strftime('%Y-%m-%d %H:%M')

        data = []
        
        if len(energyData)==0:
            abort(404, description = "No data found")
        else:
            for i in range(len(energyData)):
                energyDate = energyData[i].getTime()
                energyDateTimestamp = datetime.fromtimestamp(energyDate)
                twentyfourHourFormat = energyDateTimestamp.strftime('%Y-%m-%d %H:%M')

                if(twentyfourHourFormat > currentDate_hoursFormat and twentyfourHourFormat < currentDateFormat):
                    twelveHourTime = energyDateTimestamp.strftime('%I:%M %p')

                    data.append({
                        'labels': twelveHourTime,
                        'datetime': twentyfourHourFormat,
                        'values': energyData[i].getP1()
                    })
            
            if len(data) > 0:
                return data
            else:
                abort(404, description = "No data found")