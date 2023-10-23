import paho.mqtt.client as mqtt
import os
import csv

from utils import write_to_csv

ERROR_MESSAGE = "ESP32_ERROR"
ESP32_SUBSCRIBE_TOPIC = "esp32/main"
ESP32_PUBLISH_TOPIC = "helloo/main"
CSV_FILENAME = "test.csv"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code: {str(rc)}")
    print(f"Subscribed to topic: {ESP32_SUBSCRIBE_TOPIC}")
    client.subscribe(ESP32_SUBSCRIBE_TOPIC)

def on_message(client, userdata, message):
    payload_str = message.payload.decode('utf-8')
    print(payload_str)
    
    write_to_csv(CSV_FILENAME)
    
    client.publish(ESP32_PUBLISH_TOPIC, "test")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()
