from flask import request, abort, jsonify
from app.energy import bp
from app.energy.controller import EnergyController

energyController = EnergyController()

# Fetch Consumption data from Raspberry Pi and insert in database.
@bp.route('/consumption/fetch', methods=['POST'])
def fetchConsumptionData():
    
    energyController.fetchConsumptionData()
    return 'Successfully fetched energy consumption data from the Raspberry Pi and insterted it into the database!'

# Fetch Production data from Raspberry Pi and insert in database.
@bp.route('/production/fetch', methods=['POST'])
def fetchProductionData():
    
    energyController.fetchProductionData()
    return 'Successfully fetched energy production data from the Raspberry Pi and insterted it into the database!'
