# MQTT related
ERROR_MESSAGE = "ESP32_ERROR"
ROWS_TO_KEEP = 70
ESP32_PUBLISH_TOPIC = "home/response"

# CSV Files Related
GLOBAL_JSON_KEYS = ['time', 'pir', "light", 'ultrasonic', "temperature", "humidity", 'pressure']

FEATURE_COLS = ['pir', 'light', 'ultrasonic', 'pressure', 'temperature', 'humidity']

ESP32_SUBSCRIBE_TOPIC = "home/input"
JSON_KEYS = ['time', 'pir', "light", 'ultrasonic', "temperature", "humidity"]
DYNAMIC_CSV_FILENAME = "esp32_dynamic.csv"
MASTER_CSV_FILENAME = "esp32_main.csv"

PRESSURE_ESP32_SUBSCRIBE_TOPIC = "pressure/input"
PRESSURE_JSON_KEYS = ["pressure"]
PRESSURE_DYNAMIC_CSV_FILENAME = "esp32_dynamic_pressure.csv"
PRESSURE_MASTER_CSV_FILENAME = "esp32_main_pressure.csv"

# ESP32cam related
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
TARGET_FILENAME = 'esp32_cam_image.jpeg'

# misc
TEST_HEADERS = ['header1', 'header2', 'header3']
TEST_DATA = {
    'header1': 'value1',
    'header2': 'value2',
    'header3': 'value3'
}
MAX_ROWS = 70

# telegram related
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_CK = os.environ.get("CHAT_ID_CK")
TELEGRAM_ELLIA = os.environ.get("CHAT_ID_ELLIA")
TELEGRAM_KEVIN = os.environ.get("CHAT_ID_KEVIN")
TELEGRAM_HANNAH = os.environ.get("CHAT_ID_HANNAH")
TELEGRAM_GORDON = os.environ.get("CHAT_ID_GORDON")