import os
import csv
from dotenv import load_dotenv
import requests
import pandas as pd
import json

from constants import *

load_dotenv()

bot_token = os.environ.get("BOT_TOKEN")
chat_id = os.environ.get("CHAT_ID_CK")
 
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
    rows_df = df.tail(number_of_rows).to_dict(orient = 'records')
    features_lists = [[row[key] for row in rows_df] for key in JSON_KEYS]
    
    df = pd.read_csv(csv_dynamic_path_pressure, names=PRESSURE_JSON_KEYS).dropna()
    rows_df = df.tail(number_of_rows).to_dict(orient = 'records')
    new_row = [row[key] for row in rows_df for key in PRESSURE_JSON_KEYS] 
    features_lists.append(new_row)

    return features_lists
            
def send_telegram_message(message):
    apiURL = f'https://api.telegram.org/bot{bot_token}/sendMessage'

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