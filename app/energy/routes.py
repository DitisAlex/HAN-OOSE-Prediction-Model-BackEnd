from flask import json, request, abort, jsonify
from app.energy import bp
from app.energy.controller import EnergyController

energyController = EnergyController()


@bp.route('/consumption', methods=['GET'])
def getConsumptionData():
    data = energyController.getEnergyData('consumption')
    return jsonify(data)


# Fetch Consumption data from Raspberry Pi and insert in database
@bp.route('/consumption/fetch', methods=['POST'])
def fetchConsumptionData():
    energyController.fetchEnergyData('consumption')
    return 'Successfully fetched energy consumption data from the Raspberry Pi and insterted it into the database!'


@bp.route('/production', methods=['GET'])
def getProductionData():
    data = energyController.getEnergyData('production')
    return jsonify(data)


# Fetch Production data from Raspberry Pi and insert in database.
@bp.route('/production/fetch', methods=['POST'])
def fetchProductionData():
    energyController.fetchEnergyData('production')
    return 'Successfully fetched energy production data from the Raspberry Pi and insterted it into the database!'
