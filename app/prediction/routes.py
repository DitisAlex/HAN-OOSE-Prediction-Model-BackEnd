from flask import jsonify, request
from app.prediction import bp
from app.prediction.controller import PredictionController

from flask import jsonify

@bp.route('', methods=['GET'])
def getPrediction():

    hours = int(request.args.get('hours')) # get query param 'hours', for amount of (hour based) predictions

    predictionController = PredictionController()
    results = predictionController.getProductionPrediction(hours)

    return jsonify(results)
