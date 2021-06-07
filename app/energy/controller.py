from app.energy.dao import EnergyDAO
from app.energy.domain import EnergyPoint
from app.core.db import get_db
from flask import abort

class EnergyController:
    def __init__(self):
        self.energyDAO = EnergyDAO()
        pass

    def getEnergyData(self, type):
        energyData = self.energyDAO.getEnergyData(type)
        return energyData

    def fetchEnergyData(self, type):
        data = self.energyDAO.fetchEnergyData(type)
        self.energyDAO.insertEnergyData(type, data)
