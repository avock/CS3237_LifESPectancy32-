import os, sys, joblib
import pandas as pd
import numpy as np
# import xgboost as xgb
from sklearn.metrics import mean_squared_error

# workaround for library import issue
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from utils import read_csv
from constants import GLOBAL_JSON_KEYS, FEATURE_COLS

def df_time_preprocess(df):
    temp_df = df.copy()

    temp_df["time"] = pd.to_datetime(temp_df["time"], format='%H:%M:%S')

    temp_df["hour_of_day"] = temp_df["time"].dt.strftime("%H")
    temp_df['minute_of_day'] = temp_df['time'].dt.strftime('%M')
    
    temp_df["hour_of_day"] = pd.to_numeric(temp_df["hour_of_day"])
    temp_df["minute_of_day"] = pd.to_numeric(temp_df["minute_of_day"])

    temp_df['minute_of_day'] = temp_df['hour_of_day'] * 60 + temp_df['minute_of_day']
    temp_df = temp_df.drop(columns=['time'])
    
    temp_df['hour_of_day'] = temp_df['hour_of_day'] / 24.0
    temp_df['minute_of_day'] = temp_df['minute_of_day'] / 1440.0

    return temp_df

class RegModel:
    
    feature_thresholds = {
        'pir': {'lower': 0.4, 'upper': 0.8},
        'light': {'lower': 0.3, 'upper': 0.6},
        'ultrasonic': {'lower': 0.2, 'upper': 0.4},
        'pressure': {'lower': 0.3, 'upper': 0.7},
        'temperature': {'lower': 0.2, 'upper': 0.8},
        'humidity': {'lower': 0.2, 'upper': 0.8},
    }
    
    def __init__(self):
        
        models_folder = 'models'
        
        self.loaded_models = {}
        # FEATURES_COLS here instead of GLOBAL_JSON_KEYS as time does not have a model
        for feature in FEATURE_COLS:
            model_filename = os.path.join('src', 'ML', models_folder, f'{feature}_model.pkl')
            self.loaded_models[feature] = joblib.load(model_filename)
    
    def predict(self, new_data):
        predictions = {}
        for feature, model in self.loaded_models.items():
            predictions[feature] = model.predict(new_data[['hour_of_day', 'minute_of_day']])
        return predictions
    
    def read_data(self):
        results = {}
        for idx, cols in enumerate(GLOBAL_JSON_KEYS):
            results[cols] = read_csv(5)[idx]

        df = pd.DataFrame(results)
        df = df_time_preprocess(df)
        df['pir'] = df['pir_state']
        df = df.drop(columns = ['pir_state'])
        
        non_feature_cols = [col for col in df.columns if col not in FEATURE_COLS]
        df = df[FEATURE_COLS + non_feature_cols]
        
        return df
    
    def get_mse(self, df):
        features_mse = {}

        for feature in FEATURE_COLS:
            feature_test_data = df.loc[:, feature]
            loaded_model = self.loaded_models[feature]
            
            predictions = loaded_model.predict(df[['hour_of_day', 'minute_of_day']])
            if feature not in ['temperature', 'humidity']:
                upper_threshold = self.feature_thresholds[feature]['upper']
                lower_threshold = self.feature_thresholds[feature]['lower']

                predictions = np.where(predictions > upper_threshold, 1, predictions)
                predictions = np.where(predictions < lower_threshold, 0, predictions)
            
            predictions = predictions.reshape(-1, 1)
            
            print(feature, predictions)
            mse = mean_squared_error(feature_test_data, predictions)
            
            features_mse[feature] = mse
            
        return features_mse
