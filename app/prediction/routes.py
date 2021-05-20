from flask import jsonify, request
from app.prediction import bp
from app.prediction.controller import PredictionController

from flask import jsonify

@bp.route('', methods=['GET'])
def getPrediction():

    try:
        if 'hours' in request.args:
            hours = int(request.args.get('hours')) # get query param 'hours', for amount of (hour based) predictions
        else:
            return "Missing query parameter 'hours'", 400
    except ValueError:
        return "Query parameter 'hours' needs an integer from 1 to 4", 400

    if (hours > 4 or hours < 1):
        return "Query parameter 'hours' needs an integer from 1 to 4", 400

    predictionController = PredictionController()
    results = predictionController.getProductionPrediction(hours)

    return jsonify(results)
