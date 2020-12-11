import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

mqttBroker = "broker.hivemq.com"

client = mqtt.Client("Temperature_Inside")
client.connect(mqttBroker)

while True:
    randNumber = uniform(20.0, 21.0)
    client.publish("TEMPERATURE", randNumber)
    print(f"Just published {str(randNumber)} to topic TEMPERATURE.")
    time.sleep(1)