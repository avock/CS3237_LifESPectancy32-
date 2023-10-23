import os
import csv

ERROR_MESSAGE = "ESP32_ERROR"
ESP32_SUBSCRIBE_TOPIC = "esp32/main"
ESP32_PUBLISH_TOPIC = "helloo/main"
CSV_PATH = "test.csv"
CSV_HEADERS = ['header1', 'header2', 'header3']

def write_to_csv(data, csv_filename, headers):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, ".."))
    data_dir = os.path.join(parent_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    csv_file_path = os.path.join(data_dir, csv_filename)

    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)

    with open(csv_file_path, mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([data.get(header, '') for header in headers])

# Example data to write to the CSV
data = {
    'header1': 'value1',
    'header2': 'value2',
    'header3': 'value3'
}

# Call write_to_csv with the data
write_to_csv(data, CSV_PATH, CSV_HEADERS)
