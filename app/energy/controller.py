from app.energy.dao import EnergyDAO
from app.energy.domain import EnergyPoint
from app.core.db import get_db
from flask import abort

class EnergyController:
    def __init__(self):
        self.energyDAO = EnergyDAO()
        pass

    def getEnergyData(self, type):
        table = 'energy_consumption' if type == 'consumption' else 'energy_production'
        fetch_query = 'SELECT * FROM %s' % table

        db = get_db()
        cursor = db.cursor()
        cursor.execute(fetch_query)
        rows = cursor.fetchall()

        data = []
        if len(rows)==0:
            abort(404, description = "No data found")
        else:
            for row in rows:
                energyPoint = [x for x in row]
                data.append(
                    EnergyPoint(energyPoint[0],energyPoint[1], energyPoint[2], energyPoint[3], energyPoint[4], energyPoint[5], energyPoint[6],
                    energyPoint[7], energyPoint[8], energyPoint[9], energyPoint[10], energyPoint[11], energyPoint[12], energyPoint[13],
                    energyPoint[14], energyPoint[15], energyPoint[16], energyPoint[17], energyPoint[18], energyPoint[19], energyPoint[20])
                )
        
        energyData = self.energyDAO.getEnergyData(data)
        return energyData

    def fetchEnergyData(self, type):
        data = self.energyDAO.fetchEnergyData(type)
        self.energyDAO.insertEnergyData(type, data)
