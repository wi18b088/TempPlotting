import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print(f"received message: {str(message.payload.decode('utf8'))}")

mqttBroker = "broker.hivemq.com"

client = mqtt.Client("Smartphone")
client.connect(mqttBroker)

client.loop_start()
print("Waiting for messages...")

client.subscribe("TEMPERATURE")
client.on_message=on_message

time.sleep(30)
client.loop_stop()