from flask import jsonify, request
from datetime import datetime, timedelta
from app.prediction import bp
from app.prediction.controller import PredictionController

@bp.route('', methods=['GET'])
def getPrediction():

    try:
        if 'hours' in request.args:
            hours = int(request.args.get('hours')) # get query param 'hours', for amount of (hour based) predictions
        else:
            return "Missing query parameter 'hours'", 400
    except ValueError:
        return "Query parameter 'hours' needs an integer, but the supplied value was not an integer", 400

    if (hours > 4 or hours < 1):
        return "Query parameter 'hours' needs a value from 1 to 4", 400

    predictionController = PredictionController()
    results = predictionController.getProductionPrediction(hours)

    if (len(results) == 0):
        return "Not enough historical data to make a prediction", 404

    predictionData = []

    for predictionPoint in results:
        predictionData.append({
                    'labels': predictionPoint.getPredictedDate().strftime('%I:%M %p'),
                    'datetime': predictionPoint.getPredictedDate().strftime('%Y-%m-%d %H:%M'),
                    'value': predictionPoint.getPrediction()
                })
        

    return jsonify(predictionData)
    