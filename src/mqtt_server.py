import paho.mqtt.client as mqtt
import os
import csv
import json

from utils import write_to_csv, send_telegram_message, process_json_payload

ERROR_MESSAGE = "ESP32_ERROR"
ESP32_SUBSCRIBE_TOPIC = "home/input"
ESP32_PUBLISH_TOPIC = "home/response"
CSV_FILENAME = "test.csv"
JSON_KEYS = ["photoresistor", "pir_state", "ultrasonic_distance_cm", "temperature", "humidity"]

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code: {str(rc)}")
    print(f"Subscribed to topic: {ESP32_SUBSCRIBE_TOPIC}")
    client.subscribe(ESP32_SUBSCRIBE_TOPIC)

def on_message(client, userdata, message):
    payload_str = message.payload.decode('utf-8')
    payload_json = json.loads(payload_str)

    data = process_json_payload(payload_json, JSON_KEYS)
    write_to_csv(CSV_FILENAME, JSON_KEYS, data)
    send_telegram_message(data)
    
    client.publish(ESP32_PUBLISH_TOPIC, "1")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()
