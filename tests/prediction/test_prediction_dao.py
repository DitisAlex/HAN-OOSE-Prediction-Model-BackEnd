from app.prediction.dao import PredictionDAO
from app.prediction.domain import PredictionPoint
from app.core.db import get_db, init_db
from datetime import datetime, timedelta

def test_insertPrediction(app):
    # Arrange
    sql_query = 'SELECT COUNT(predicted_on) FROM prediction_data'
    predictionPoint = PredictionPoint(datetime.fromtimestamp(1619161200), datetime.fromtimestamp(1619163914), 323.2) # 2021-04-23 9:00:00, 2021-04-21 9:45:14
    with app.app_context():
        init_db()  # Empty the database before running this tests.
    predictionDAO = PredictionDAO()

    # Act
    with app.app_context():
        predictionDAO.insertPrediction(predictionPoint)
        db = get_db()
        count = db.execute(sql_query).fetchone()[0]

    # Assert
    assert count > 0


def test_deleteNewerPredictions(app):
    # Arrange
    predictionDAO = PredictionDAO()
    sql_query = 'SELECT COUNT(predicted_on) FROM prediction_data'\
    
    currentTime = datetime.now()
    newerTime = currentTime + timedelta(hours=1)

    newerPredictionPoint = PredictionPoint(currentTime, newerTime, 10)

    with app.app_context():
        init_db()  # Empty the database before running this tests.

    # # Act
    with app.app_context():
        predictionDAO.insertPrediction(newerPredictionPoint)
        predictionDAO.deleteNewerPredictions(currentTime)
        db = get_db()
        count = db.execute(sql_query).fetchone()[0]

    # Assert
    assert count == 0