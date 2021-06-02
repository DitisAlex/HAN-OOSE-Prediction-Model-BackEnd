from app.energy.controller import EnergyController
from app.energy.dao import EnergyDAO

def test_getConsumptionData(app):
    # Arrange
    energyDAO = EnergyDAO()

    energyData = [{'labels': '07:36 AM', 'datetime': '2021-05-25 07:36', 'values': 0.0}, {'labels': '08:36 AM', 'datetime': '2021-05-25 08:36', 'values': 0.0}]

    # # Act
    with app.app_context():
        data = energyDAO.getEnergyData(energyData)

    # Assert
    assert len(data) > 0

def test_getProductionData(app):
    # Arrange
    energyDAO = EnergyDAO()

    energyData = [{'labels': '03:36 AM', 'datetime': '2021-05-25 03:36', 'values': 0.0}, {'labels': '04:36 AM', 'datetime': '2021-05-25 04:36', 'values': 0.0}]

    # # Act
    with app.app_context():
        data = energyDAO.getEnergyData(energyData)

    # Assert
    assert len(data) > 0