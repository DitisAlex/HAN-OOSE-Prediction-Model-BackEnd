from app.energy.dao import EnergyDAO

class EnergyController:
    def __init__(self):
        self.energyDAO = EnergyDAO()
        pass

    def getEnergyData(self, type):
        data = self.energyDAO.getEnergyData(type)
        return data

    def fetchEnergyData(self, type):
        data = self.energyDAO.fetchEnergyData(type)
        self.energyDAO.insertEnergyData(type, data)