from flask import jsonify, abort
from app.energy import bp
from app.energy.controller import EnergyController

energyController = EnergyController()


@bp.route('/consumption', methods=['GET'])
def getConsumptionData():
    data = energyController.getEnergyData('consumption')

    if (len(data) < 1):
        abort(404, "no data!")

    return jsonify(data)


@bp.route('/production', methods=['GET'])
def getProductionData():
    data = energyController.getEnergyData('production')

    if (len(data) == 0):
        abort(404, "no data!")

    return jsonify(data)
