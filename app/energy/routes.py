from flask import jsonify
from app.energy import bp
from app.energy.controller import EnergyController

energyController = EnergyController()

@bp.route('/consumption', methods=['GET'])
def getConsumptionData():
    data = energyController.getEnergyData('consumption')
    return jsonify(data)

@bp.route('/production', methods=['GET'])
def getProductionData():
    data = energyController.getEnergyData('production')
    return jsonify(data)
