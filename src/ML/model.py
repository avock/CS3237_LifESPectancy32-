import os, sys, joblib
import xgboost as xgb

# workaround for library import issue
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from utils import read_csv
from constants import FEATURE_COLS

class RegressionModel:
    def __init__(self):
        
        models_folder = 'models'
        
        self.loaded_models = {}
        for feature in FEATURE_COLS:
            model_filename = os.path.join('src', 'ML', models_folder, f'{feature}_model.pkl')
            self.loaded_models[feature] = joblib.load(model_filename)

        self.get_data = read_csv
    
    def predict(self, new_data):
        predictions = {}
        for feature, model in self.loaded_models.items():
            predictions[feature] = model.predict(new_data[['hour_of_day', 'minute_of_day']])
        return predictions
    
    def test(self):
        return 'test'