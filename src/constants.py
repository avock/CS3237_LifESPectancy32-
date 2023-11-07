# MQTT related
ERROR_MESSAGE = "ESP32_ERROR"
ESP32_SUBSCRIBE_TOPIC = "home/input"
ESP32_PUBLISH_TOPIC = "home/response"
CSV_FILENAME = "esp32_main.csv"
JSON_KEYS = ["photoresistor", "pir_state", "ultrasonic_distance_cm", "temperature", "humidity"]

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