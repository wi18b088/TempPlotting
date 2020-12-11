import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

mqttBroker = "broker.hivemq.com"

client = mqtt.Client("Temperature_Inside")
client.connect(mqttBroker)

while True:
    randNumber = uniform(18.0, 27.0)
    client.publish("TEMPDISPLAY", randNumber)
    print(f"Just published {str(randNumber)} to topic TEMPDISPLAY.")
    time.sleep(1)