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
from pyowm.owm import OWM
from pyowm.utils import timestamps, formatting
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
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
        PATH = "instance/models/Clear_sky_update.pt"

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
        self.sc_X=load('instance/models/scaler_X_Clear_sky_update.bin')
        self.sc_Y=load('instance/models/scaler_Y_Clear_sky_update.bin')
        self.sc_W=load('instance/models/scaler_W_Clear_sky_update.bin')


    def makePrediction(self, hours):

        # Get historical PV data
        PV_data = self.energyDAO.getDataForPrediction()


        if (len(PV_data) < 4):
            return []


        ######## Pytorch code starts here ########

        
        # weather keys
        key ='1a4df9d4817c3d16e92b272d59531753'
        pass_hours = 12
        future_data = 24

        # cyclic data keys
        tz = 'UTC'
        lat, lon = 51.98787601885725, 5.950209138832937
        first_doy= '1/1/2021'
        first_dony = '01/01/2022'
        
        # Get pass weather data
        passweather = self.get_history_weather(key, pass_hours)
    
        # Get future weather data
        futureweather = self.get_future_weather(key, future_data)

        Power = PV_data['P1'].values
        Power = np.reshape(Power, (-1, 1))[0:12]
        Power = np.nan_to_num(Power)

        # get cyclic data
        cyclic_ = self.cyclic_data(tz,lat,lon,first_doy,first_dony)
        
        # get current cyclic data
        current_c_data = self.get_current_cyclic_data(cyclic_,PV_data)
        
        # get future cyclic data
        future_cyclic_data = self.get_future_cyclic_data(cyclic_,future_data)

        # Stack Power, Temperaure and Cloud data together.
        input_data = np.hstack((Power,passweather, current_c_data))
        input_data[:,9] = input_data[:,9]*(1-(input_data[:,2]/9 * input_data[:,4]))
        input_data = self.sc_X.transform(input_data)
        input_data = input_data.reshape((1,input_data.shape[0], input_data.shape[1]))

        # Convert data into torch tensor 
        input_data = Variable(torch.Tensor(np.array(input_data)))

        # Weather data
        Weather = np.hstack((futureweather, future_cyclic_data))
        Weather[:,8] = Weather[:,8]*(1-(Weather[:,1]/9 * Weather[:,3]))
        Weather = self.sc_W.transform(Weather)
        Weather = Variable(torch.Tensor(np.array(Weather)))

        #Create an empty array
        predict =np.array([])

        for i in range(hours): # The number of prediction steps ---- Set this to the given hours parameter. -v
            
            # call the model for predicting the Solar power in the next hour.
            
            Predic_P = self.model(input_data)
            
            # Use the predicted value to predict the next steps (2nd,3rd....) hours
            
            if i < len(Weather):
                Predic_W = Weather[i+1]
            else:
                Predic_W = Variable(torch.Tensor(np.array([0, 0,0])))
            
            # Add the predicted values to the input set for the next prediction points.
            # Remove the 1st row, return to 24 points input
            
            new_input_data =  torch.vstack((input_data[0,:,0:11],torch.cat((Predic_P[0],Predic_W),0)))
            new_input_data =  new_input_data[torch.arange (new_input_data.size (0))!=0]
            
            input_data[0] = new_input_data
            
            # Add all prediction value together. 
            Predic_P = Predic_P.detach().numpy()  
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


    def cyclic_data(self, tz,lat,lon,first_doy,first_dony):
        
        """ Arg:
            - tz         :     time zone
            - lat        :     latitude
            - lon        :     longitude
            - first_doy  :     first day of the year
            - first_dony :     first day of next year
    
        Returns:
            - clearsky   : dataframe with clear sky of the year and clyclic_data
            
            https://towardsdatascience.com/cyclical-features-encoding-its-about-time-ce23581845ca
            https://ianlondon.github.io/blog/encoding-cyclical-features-24hour-time/
            https://www.datasciencecentral.com/profiles/blogs/how-to-make-time-data-cyclical-for-prediction
            
        """
        # Create location object to store lat, lon, timezone
        site = location.Location(lat, lon, tz=tz)

        times = pd.date_range(start=first_doy, end=first_dony, freq='1H',tz=site.tz)
        idx =  pd.DataFrame(times.to_pydatetime(),columns =['Time'])
        idx['year']  = idx['Time'].apply(lambda x:x.year)
        idx['month'] = idx['Time'].apply(lambda x:x.month)
        idx['day']   = idx['Time'].apply(lambda x:x.day)
        idx['hour']  = idx['Time'].apply(lambda x:x.hour)

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
        idx['hour_sin']      = self.sin_transform(idx['hour'])
        idx['hour_cos']      = self.cos_transform(idx['hour'])

        
        #times    
        clearsky = site.get_clearsky(times)
        
        # shift 1 hour up for correction   
        clearsky['ghi'] = clearsky['ghi'].shift(-1)
        clearsky['ghi'] = clearsky['ghi'].fillna(0)
        
        # drop dni and dhi
        clearsky.drop(['dni','dhi'],axis=1, inplace=True) #updating the same dataframe by dropping two columnsclearsky2021.reset_index(inplace=True)
        clearsky.reset_index(inplace=True)
        clearsky['index'] = clearsky['index'].apply(lambda x:x.to_pydatetime())
        clearsky['year']  = clearsky['index'].apply(lambda x:x.year)
        clearsky['month'] = clearsky['index'].apply(lambda x:x.month)
        clearsky['day']   = clearsky['index'].apply(lambda x:x.day)
        clearsky['hour']  = clearsky['index'].apply(lambda x:x.hour)

        cyclic_data = pd.merge(clearsky,idx, on=['year','month','day','hour'])
        cyclic_data['ghi']=cyclic_data['ghi'].values*11.52
        
        return cyclic_data

    def get_current_cyclic_data(self, cyclic_data,solar_data):
    
        """ Arg:
            - cyclic_data         :     cyclic data
            - solar_data          :     PV input data
        
        Returns:
            - pass_cyclic   : get n hours (the number of hours = number of pass PV hours) 
                            to current time of cyclic data    
        """

        solar_data['index'] = solar_data.index        # I rewrote the following code because, as it was, it was trying to execute these functions on the indexes (see Kaggle for context). -v
        solar_data['time'] = solar_data['time'].apply(lambda x:datetime.utcfromtimestamp(x)) # !IMPORTANT! I'm not sure if this gives the right timezone. If timezone issues: check here! -v
        solar_data['year']  = solar_data['time'].apply(lambda x:x.year)
        solar_data['month'] = solar_data['time'].apply(lambda x:x.month)
        solar_data['day']   = solar_data['time'].apply(lambda x:x.day)
        solar_data['hour']  = solar_data['time'].apply(lambda x:x.hour)
    
        current_cyclic = pd.merge(solar_data,cyclic_data, on=['year','month','day','hour'])
        current_cyclic.drop(current_cyclic.columns.difference(['dayofyear_sin',
                                                            'dayofyear_cos','hour_sin',
                                                            'hour_cos','ghi']), 1, inplace=True)
        
        current_cyclic = current_cyclic[["dayofyear_sin", "dayofyear_cos", 
                                        "hour_sin","hour_cos","ghi"]]
        
        return current_cyclic.head(12) # Needed to cut these so I could np stack them later (arrays need to be same size to stack). -v

    def get_future_cyclic_data(self, cyclic_data,hours):
    
        """ Arg:
        
            - cyclic_data         :     cyclic_data
            - hours               :     number of future data
        
        Returns:
            - future_cyclic_data  : get n hours  of future cyclic data    
        """
        
        doy_temp = pd.DataFrame(columns = ['temp'])
        future_hours = []

        for i in range(hours):

            temp = datetime.utcnow().replace(microsecond=0, second=0, minute=0) + timedelta(hours=i+1)
            future_hours = np.append(future_hours,temp)
            doy_temp.loc[future_hours[i]]= 0

            doy_temp['index'] = doy_temp.index
            doy_temp['index'] = doy_temp['index'].apply(lambda x:x.to_pydatetime())
            doy_temp['year']  = doy_temp['index'].apply(lambda x:x.year)
            doy_temp['month'] = doy_temp['index'].apply(lambda x:x.month)
            doy_temp['day']   = doy_temp['index'].apply(lambda x:x.day)
            doy_temp['hour']  = doy_temp['index'].apply(lambda x:x.hour)

        future_cyclic_data = pd.merge(doy_temp, cyclic_data, on=['year','month','day','hour'])
        
        future_cyclic_data.drop(future_cyclic_data.columns.difference(['dayofyear_sin','dayofyear_cos',
                                                                    'hour_sin','hour_cos','ghi']), 1, inplace=True)
        
        future_cyclic_data = future_cyclic_data[["dayofyear_sin", "dayofyear_cos", 
                                                "hour_sin","hour_cos","ghi"]]
    
        return future_cyclic_data

    def get_history_weather(self,key,pass_hours):

        DATETIME_FORMAT = '%Y-%m-%d %H:%M'
    
        owm = OWM(key)
        mgr = owm.weather_manager()
        
        # what is the epoch for yesterday at this time?
        
        yesterday_epoch = formatting.to_UNIXtime(timestamps.yesterday())
        one_call_yesterday = mgr.one_call_history(lat=51.98787601885725, lon=5.950209138832937, dt=yesterday_epoch)
        
        # today weather up to current time
        
        today = int((datetime.utcnow() - timedelta(hours=1)).replace(tzinfo=timezone.utc).timestamp())
        one_call_today = mgr.one_call_history(lat=51.98787601885725, lon=5.950209138832937, dt=today)
        
        weather = pd.DataFrame(columns = ['temperature','cloud','wind','rain'])
        
        for i in range(len(one_call_yesterday.forecast_hourly)):

            temp    = one_call_yesterday.forecast_hourly[i].ref_time
            temp    = datetime.fromtimestamp(temp).strftime(DATETIME_FORMAT)
            cloud   = one_call_yesterday.forecast_hourly[i].clouds
            cloud   = np.rint(cloud*8/100)
            temperature = one_call_yesterday.forecast_hourly[i].temperature('celsius')['temp']
            wind   = one_call_yesterday.forecast_hourly[i].wind()['speed']

            if one_call_yesterday.forecast_hourly[i].status == 'rain':
                    rain = 1
            else: rain = 0

            weather = weather.append({'temperature': temperature,'cloud': cloud,
                                    'wind': wind,'rain': rain},ignore_index=True)

        for i in range (len(one_call_today.forecast_hourly)):

            temp    = one_call_today.forecast_hourly[i].ref_time
            temp    = datetime.fromtimestamp(temp).strftime(DATETIME_FORMAT)
            cloud   = one_call_today.forecast_hourly[i].clouds
            cloud   = np.rint(cloud*8/100)
            temperature = one_call_today.forecast_hourly[i].temperature('celsius')['temp']
            wind   = one_call_today.forecast_hourly[i].wind()['speed']

            if one_call_today.forecast_hourly[i].status == 'rain':
                    rain = 1
            else: rain = 0


            weather = weather.append({'temperature': temperature,'cloud': cloud,
                                    'wind': wind,'rain': rain},ignore_index=True)
        
        weather = weather.tail(pass_hours)
        weather.reset_index(drop=True, inplace=True)
        return weather

    def get_future_weather(self,key,future_hours):
        
        owm = OWM(key)
        mgr = owm.weather_manager()
        one_call_future = mgr.one_call(lat=51.98787601885725, lon=5.950209138832937)
        

        future_weather = pd.DataFrame(columns = ['temperature','cloud','wind','rain'])

        for i in range(len(one_call_future.forecast_hourly)):

            temp        = one_call_future.forecast_hourly[i].ref_time
            temp        = datetime.fromtimestamp(temp).strftime('%Y-%m-%d %H:%M:%S')
            cloud       = one_call_future.forecast_hourly[i].clouds
            cloud       = np.rint(cloud*8/100)
            temperature = one_call_future.forecast_hourly[i].temperature('celsius')['temp']
            wind        = one_call_future.forecast_hourly[i].wind()['speed']

            if one_call_future.forecast_hourly[i].status == 'rain':
                    rain = 1
            else: rain = 0

            future_weather = future_weather.append({'temperature': temperature,'cloud': cloud,
                                                    'wind': wind,'rain': rain},ignore_index=True)

        future_weather = future_weather[1:future_hours+1]
        return future_weather