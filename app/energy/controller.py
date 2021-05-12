from app.energy.dao import EnergyDAO

class EnergyController:
    def __init__(self):
        self.energyDAO = EnergyDAO()
        pass

    def fetchConsumptionData(self):
        data = self.energyDAO.fetchData('consumption')
        self.energyDAO.insertData('consumption', data)

        return ''

    def fetchProductionData(self):
        data = self.energyDAO.fetchData('production')
        self.energyDAO.insertData('production', data)

        return ''