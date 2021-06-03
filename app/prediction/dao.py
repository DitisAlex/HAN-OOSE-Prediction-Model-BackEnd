from app.core.db import get_db, get_rpi_db

class PredictionDAO:
  def __init__(self):
    pass

  def insertPrediction(self, predictionPoint):

    # Open database
    db = get_db()
    cur = db.cursor()

    query = '''INSERT INTO prediction_data (predicted_on, predicted_date, prediction) VALUES (?,?,?)'''
    values = (
                predictionPoint.getPredictedOn().strftime('%Y-%m-%d %H:%M:%S'),
                predictionPoint.getPredictedDate().strftime('%Y-%m-%d %H:%M:%S'),
                predictionPoint.getPrediction())
                
    cur.execute(query, values)

  def deleteNewerPredictions(self, datetime):
      
    # Open database
    db = get_db()
    cur = db.cursor()

    query = '''DELETE FROM prediction_data WHERE predicted_date > ?'''
    values = (str(datetime),)

    cur.execute(query, values)
      
