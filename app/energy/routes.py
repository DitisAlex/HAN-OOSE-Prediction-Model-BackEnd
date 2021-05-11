from flask import request, abort
from app.energy import bp
from app.energy.controller import EnergyController

from flask import jsonify


@bp.route('/consumption', methods=['GET'])
def insertConsumption():
    c = EnergyController()

    try:
        data = c.getConsumptionData()
        # c.insertConsumptionData(data)

        return "Correctly inserted consumption data"
    except KeyError:  # KeyError = missing key in json
        abort(401, "Invalid data")


@bp.route('/production', methods=['GET'])
def insertProduction():
    c = EnergyController()

    try:
        data = c.getProductionData()
        c.insertProductionData(data)

        return "Correctly inserted production data"
    except KeyError:  # KeyError = missing key in json
        abort(401, "Invalid data")
