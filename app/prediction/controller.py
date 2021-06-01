from numpy.lib.function_base import append
from app.prediction.dao import PredictionDAO
from app.energy.dao import EnergyDAO
from app.prediction.domain import PredictionPoint
from app.prediction.predictionmodel import LSTM
from app.weather.controller import WeatherController

import torch
from joblib import load
from torch.autograd import Variable
from pvlib import location
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import numpy as np


class PredictionController:
    def __init__(self):
        self.predictionDAO = PredictionDAO()
        self.energyDAO = EnergyDAO()
        self.weatherController = WeatherController()
        pass

    def getProductionPrediction(self, hours):
        predictionData = []

        self.loadModel()

        result = self.makePrediction(hours)

        if (len(result) == 0):
            return result

        currentTime = datetime.now() + timedelta(hours=2) # 2 hour timezone correction

        self.predictionDAO.deleteNewerPredictions(currentTime) # if there are predictions with a time that this prediction will also cover, delete them. prevents double data.

        for i in range(hours):

            predictionTime = currentTime + timedelta(hours=i+1) # prediction starts at 1 hour from now
            
            predictionPoint = PredictionPoint(currentTime, predictionTime, result[i][0])

            self.predictionDAO.insertPrediction(predictionPoint)

            predictionData.append(predictionPoint)

        return predictionData



    def loadModel(self): # Mostly Pytorch code
        PATH = "models/KNMI_GPU_sin_cos_with_clear_sky.pt"

        # Input parameters for the model structure. These are the ones that will need customising eventually

        input_size = 10
        hidden_size = 128
        num_layers = 1
        seq_length = 24
        num_classes = 1
        bidirectional = True

        # Load
        device = torch.device('cpu')

        # Load
        device = torch.device('cpu')
        self.model = LSTM(num_classes, input_size, hidden_size, num_layers, seq_length, bidirectional)
        self.model.load_state_dict(torch.load(PATH, map_location=device))

        # Load
        self.sc_X=load('models/scaler_X_sin_cos_with_clear_sky.bin')
        self.sc_Y=load('models/scaler_Y_sin_cos _with_clear_sky.bin')
        self.sc_W=load('models/scaler_W_sin_cos _with_clear_sky.bin')


    def makePrediction(self, hours):

        weatherData = self.weatherController.getWeatherData()
        PV_data = self.energyDAO.getDataForPrediction()

        if (len(weatherData) < 4 or len(PV_data) < 4):
            return []

        Temperature = []
        Cloud = []
        Wind = []
        Press = []

        for weatherDataPoint in weatherData:
            Temperature.append(weatherDataPoint.getTemperature())
            Cloud.append(weatherDataPoint.getCloud())
            Wind.append(weatherDataPoint.getWind())
            Press.append(weatherDataPoint.getPressure())



        # Convert cloud percentages to Octant because the train values data is on Octant (0-8).

        # Cloud_Oct = np.rint(Cloud*8/100) <-- Bizzare math being executed on array. Does this ever work? Not like that in any case. Wrote a loop for it instead. -v
        Cloud_Oct = []
        for cloudPoint in Cloud:
            Cloud_Oct.append(cloudPoint*8/100)

        ######## Pytorch code kicks here ########

        Power = PV_data['P1'].values
        Power = np.reshape(Power, (-1, 1))[0:4]

        Power = np.reshape(Power, (-1, 1))[0:24]
        Temperature = np.reshape(Temperature, (-1, 1))[0:24]
        Cloud_Oct = np.reshape(Cloud_Oct, (-1, 1))[0:24]
        Wind = np.reshape(Wind, (-1, 1))[0:24]
        Press = np.reshape(Press, (-1, 1))[0:24]

        mean_T = np.mean(Temperature)
        mean_C = np.mean(Cloud_Oct)
        mean_W = np.mean(Wind)
        mean_Press = np.mean(Press)


        T = np.full((4, 1), mean_T)
        T[-1] = Temperature[0]
        C = np.full((4, 1), mean_C)
        C[-1] = Cloud_Oct[0]
        W = np.full((4, 1), mean_W)
        W[-1] = Wind[0]
        Pres = np.full((4, 1), mean_Press)
        Pres[-1] = Press[0]

        cyclic_ = self.cyclic_data(PV_data)
        C_data = self.get_current_cyclic_data(cyclic_, PV_data)
        future_data = self.get_future_cyclic_data(cyclic_)

        # Stack Power, Temperaure and Cloud data together.
        input_data = np.hstack((Power,T ,C,W,Pres,C_data.values))
        input_data = self.sc_X.transform(input_data)
        input_data = input_data.reshape((1,input_data.shape[0], input_data.shape[1]))

        # Convert data into torch tensor 
        input_data = Variable(torch.Tensor(np.array(input_data)))

        # Weather data
        #Weather = np.hstack((Temperature_sc ,Cloud_sc, Wind_sc))
        Weather = np.hstack((Temperature ,Cloud_Oct, Wind,Press, future_data.values))
        Weather = self.sc_W.transform(Weather)
        Weather = Variable(torch.Tensor(np.array(Weather)))

        # The last data point is the current weather condition.
        input_data[0,-1,1:11]= Weather[0]
        Predic_W = Weather[0]

        #Create an empty array
        predict =np.array([])

        for i in range(hours): # The number of prediction steps ---- Set this to the given hours parameter. -v
            
            # call the model for predicting the Solar power in the next hour.
            
            Predic_P = self.model(input_data)
            
            # Use the predicted value to predict the next steps (2nd,3rd....) hours
            
            if i < len(Weather):
                #Predic_W = Weather[0:i+1]
                Predic_W = Weather[i+1]
            else:
                Predic_W = Variable(torch.Tensor(np.array([0, 0,0])))
            
            # Add the predicted values to the input set for the next prediction points.
            # Remove the 1st row, return to 24 points input
            
            new_input_data =  torch.vstack((input_data[0,:,0:11],torch.cat((Predic_P[0],Predic_W),0)))
            new_input_data =  new_input_data[torch.arange (new_input_data.size (0))!=0]
            
            input_data[0] = new_input_data
            #print(input_data[0,-1,:])
            
            # Add all prediction value together. 
            Predic_P = Predic_P.detach().numpy()  
            #print(Predic_P)
            predict = np.append(predict,Predic_P)

        predict_tf = np.reshape(predict, (len(predict), 1))
        predict_tf = self.sc_Y.inverse_transform(predict_tf)         
        # Solar power always > 0
        predict_tf[predict_tf < 0] = 0

        return predict_tf.tolist()



    

    ####################### All the following functions are *almost* directly taken from the Pytorch model code #######################
    
    def sin_transform(self, values):
        return np.sin(2*np.pi*values/len(set(values)))

    def cos_transform(self, values):
        return np.cos(2*np.pi*values/len(set(values)))



    def cyclic_data(self, PV_data):
        

        PV_data['index'] = PV_data.index        # I rewrote the following code because, as it was, it was trying to execute these functions on the indexes (see Kaggle for context). -v
        PV_data['time'] = PV_data['time'].apply(lambda x:datetime.utcfromtimestamp(x)) # !IMPORTANT! I'm not sure if this gives the right timezone. If timezone issues: check here! -v
        PV_data['year']  = PV_data['time'].apply(lambda x:x.year)
        PV_data['month'] = PV_data['time'].apply(lambda x:x.month)
        PV_data['day']   = PV_data['time'].apply(lambda x:x.day)
        PV_data['hour']  = PV_data['time'].apply(lambda x:x.hour)

        tz = 'GMT'

        lat, lon = 51.98787601885725, 5.950209138832937
        # Create location object to store lat, lon, timezone
        site = location.Location(lat, lon, tz=tz)

        times2021 = pd.date_range(start='1/1/2021', end='01/01/2022', freq='1H',tz=site.tz) #tz='UTC'
        #print (idx.to_pydatetime())
        idx =  pd.DataFrame(times2021.to_pydatetime(),columns =['time'])
        idx['year']  = idx['time'].apply(lambda x:x.year)
        idx['month'] = idx['time'].apply(lambda x:x.month)
        idx['day']   = idx['time'].apply(lambda x:x.day)
        idx['hour']  = idx['time'].apply(lambda x:x.hour)

        temp=np.zeros(len(idx['day']))
        day=1
        month=1
        year=2021
        doy=1

        for i in range(len(idx['day'])):


            if idx['month'][i] > month:
                month = month + 1
                day = 0

            if idx['day'][i] > day:
                day=day+1
                doy = doy + 1

            if idx['year'][i] > year:
                year  =  year + 1
                doy   = 1
                month = 1
                day   = 1
            temp[i] = doy

        idx['doy'] = temp

        idx['dayofyear_sin'] = self.sin_transform(idx['doy'])
        idx['dayofyear_cos'] = self.cos_transform(idx['doy'])
        idx['hour_sin'] = self.sin_transform(idx['hour'])
        idx['hour_cos'] = self.cos_transform(idx['hour'])

        #times = pd.date_range(start='1/1/2021', end='01/01/2022', freq='1H',tz=site.tz)
        #times
        clearsky2021 = site.get_clearsky(times2021) # clearsky2021 = site.get_clearsky(times2021) ---- was the original line. -v
        clearsky2021.drop(['dni','dhi'],axis=1, inplace=True) #updating the same dataframe by dropping two columnsclearsky2021.reset_index(inplace=True)
        clearsky2021.reset_index(inplace=True)
        clearsky2021['index']=clearsky2021['index'].apply(lambda x:x.to_pydatetime())
        clearsky2021['year'] = clearsky2021['index'].apply(lambda x:x.year)
        clearsky2021['month'] = clearsky2021['index'].apply(lambda x:x.month)
        clearsky2021['day'] = clearsky2021['index'].apply(lambda x:x.day)
        clearsky2021['hour'] = clearsky2021['index'].apply(lambda x:x.hour)

        cyclic_data = pd.merge(clearsky2021,idx, on=['year','month','day','hour'])
        cyclic_data['ghi']=cyclic_data['ghi'].values*11.52
        
        return cyclic_data

    def get_current_cyclic_data(self, cyclic_, PV_data):
   
        C_data = pd.merge(PV_data,cyclic_, on=['year','month','day','hour'])
        C_data.drop(C_data.columns.difference(['dayofyear_sin',
                                            'dayofyear_cos',
                                            'hour_sin','hour_cos','ghi']), 1, inplace=True)
        C_data = C_data[["dayofyear_sin", "dayofyear_cos", 
                                "hour_sin","hour_cos","ghi"]]
        return C_data.head(4) #Added a head(4) to this because I don't understand why this is giving back more than 4 datapoints. (head(x) returns gives the top x points). -v

    def get_future_cyclic_data(self, cyclic_data):
        
        hours =24
        doy_temp = pd.DataFrame(columns = ['temp'])
        future_hours = []

        for i in range(hours):

            temp = datetime.now().replace(microsecond=0, second=0, minute=0) + timedelta(hours=i+1)
            future_hours = np.append(future_hours,temp)
            doy_temp.loc[future_hours[i]]= 0

            doy_temp['index'] = doy_temp.index
            doy_temp['index'] = doy_temp['index'].apply(lambda x:x.to_pydatetime())
            doy_temp['year']  = doy_temp['index'].apply(lambda x:x.year)
            doy_temp['month'] = doy_temp['index'].apply(lambda x:x.month)
            doy_temp['day']   = doy_temp['index'].apply(lambda x:x.day)
            doy_temp['hour']  = doy_temp['index'].apply(lambda x:x.hour)

        future_data = pd.merge(doy_temp, cyclic_data, on=['year','month','day','hour'])
        future_data.drop(future_data.columns.difference(['dayofyear_sin',
                                                        'dayofyear_cos',
                                                        'hour_sin','hour_cos','ghi']), 1, inplace=True)
        future_data = future_data[["dayofyear_sin", "dayofyear_cos", 
                                "hour_sin","hour_cos","ghi"]]
        
        return future_data