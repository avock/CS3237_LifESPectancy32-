import os
import csv

TEST_HEADERS = ['header1', 'header2', 'header3']
TEST_DATA = {
    'header1': 'value1',
    'header2': 'value2',
    'header3': 'value3'
}

def write_to_csv(csv_filename, headers=TEST_HEADERS, data=TEST_DATA):
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
