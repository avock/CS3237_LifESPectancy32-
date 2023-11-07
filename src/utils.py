import os
import csv
from dotenv import load_dotenv
import requests

import constants

load_dotenv()

bot_token = os.environ.get("BOT_TOKEN")
chat_id = os.environ.get("CHAT_ID_CK")

def write_to_csv(csv_filename, headers=TEST_HEADERS, data=TEST_DATA):
    script_dir = os.path.dirname(os.path.abspath(__file))
    parent_dir = os.path.abspath(os.path.join(script_dir, ".."))
    data_dir = os.path.join(parent_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    csv_file_path = os.path.join(data_dir, csv_filename)

    # Check if the file exists
    file_exists = os.path.isfile(csv_file_path)
    
    if not file_exists:
        with open(csv_file_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)
    
    with open(csv_file_path, mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        if file_exists:
            with open(csv_file_path, mode='r') as existing_file:
                existing_rows = list(csv.reader(existing_file))
                num_existing_rows = len(existing_rows)
                if num_existing_rows >= MAX_ROWS:
                    # Remove the first row (header remains)
                    existing_rows.pop(1)
                    with open(csv_file_path, mode='w', newline='') as new_file:
                        writer = csv.writer(new_file)
                        for row in existing_rows:
                            writer.writerow(row)

        writer.writerow([data.get(header, '') for header in headers])
               
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