import os
import csv
from dotenv import load_dotenv
import requests
import pandas as pd
import json

from constants import *
 
def write_to_csv(csv_dynamic, csv_main, headers=TEST_HEADERS, data=TEST_DATA):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, ".."))
    data_dir = os.path.join(parent_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    csv_dynamic_path = os.path.join(data_dir, csv_dynamic)
    csv_main_path = os.path.join(data_dir, csv_main)

    # csv files do not currently exist
    if not os.path.isfile(csv_dynamic_path):
        with open(csv_dynamic_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)
    if not os.path.isfile(csv_main_path):
        with open(csv_main_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)

    # write to dynamic (only 70 rows of data) csv
    with open(csv_dynamic_path, mode='a', newline='') as csv_dynamic_file:
        dynamic_writer = csv.writer(csv_dynamic_file)
        dynamic_writer.writerow([data.get(header, '') for header in headers])

        # Read the existing data in the dynamic CSV
        with open(csv_dynamic_path, mode='r') as csv_dynamic_read_file:
            dynamic_reader = csv.reader(csv_dynamic_read_file)
            dynamic_data = list(dynamic_reader)

        # If the dynamic CSV exceeds 70 rows (excluding headers), remove the oldest row
        if len(dynamic_data) >= ROWS_TO_KEEP:
            dynamic_data = dynamic_data[-(ROWS_TO_KEEP-1):]
            
        with open(csv_dynamic_path, mode='w', newline='') as csv_dynamic_file:
            dynamic_writer = csv.writer(csv_dynamic_file)
            dynamic_writer.writerows(dynamic_data)
            
    # write to main csv (contains all data over time)
    with open(csv_main_path, mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([data.get(header, '') for header in headers])
      
def read_csv(number_of_rows):
    
    target_csv = 'esp32_dynamic.csv'
    pressure_csv = 'esp32_dynamic_pressure.csv'
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, ".."))
    data_dir = os.path.join(parent_dir, "data")
    
    csv_dynamic_path = os.path.join(data_dir, target_csv)
    csv_dynamic_path_pressure = os.path.join(data_dir, pressure_csv)
    

    df = pd.read_csv(csv_dynamic_path, names=JSON_KEYS).dropna()
    available_rows_main = len(df)
    df_pressure = pd.read_csv(csv_dynamic_path_pressure, names=PRESSURE_JSON_KEYS).dropna()
    available_rows_pressure = len(df_pressure)
    
    number_of_rows = min(available_rows_main, available_rows_pressure)
        
    rows_df = df.tail(number_of_rows).to_dict(orient = 'records')
    features_lists = [[row[key] for row in rows_df] for key in JSON_KEYS]
    
    rows_df = df_pressure.tail(number_of_rows).to_dict(orient = 'records')
    new_row = [row[key] for row in rows_df for key in PRESSURE_JSON_KEYS] 
    features_lists.append(new_row)

    return features_lists
            
def send_telegram_message(message, chat_id=TELEGRAM_CK):
    apiURL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chat_id, 'text': message})
        # print(response.text)
    except Exception as e:
        print(e)
        
def process_json_payload(payload_json, keys):
    extracted_data = {}
    for key in keys:
        if key in payload_json:
            extracted_data[key] = payload_json[key]

    return extracted_data

def anomaly_threshold_check(features_error):
    
    feature_anomaly = {}
    
    for feature in FEATURE_COLS:
        feature_error = features_error[feature]
        
        if feature_error > feature_anomaly_thresholds[feature]:
            feature_anomaly[feature] = True
        else: 
            feature_anomaly[feature] = False
            
    return feature_anomaly

feature_anomaly_thresholds = {    
    'pir': 35,
    'light': 35,
    'ultrasonic': 35,
    'pressure': 50,
    'temperature': 10,
    'humidity': 15
}

def format_anomaly_threshold(features_error):
    
    temperature_anomaly = False
    humidity_anomaly = False
    movement_anomaly = False
    
    messages = {}
    
    if features_error['pir'] or features_error['ultrasonic'] or features_error['pressure']:
        messages['movmement'] = True
        
    if features_error['temperature']:
        messages['temperature'] = True
        
    if features_error['humidity']:
        messages['humidity'] = True
            
    return messages

def format_anomaly_message(features_anomaly):
    anomalies = []
    for key, value in features_anomaly.items():
        if value:
            anomalies.append(key.capitalize())
    message = f'[ALERT] Anomaly Detected in {", ".join(anomalies)}' if anomalies else ''
    print(anomalies)
    return message
        
