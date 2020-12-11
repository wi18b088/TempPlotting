import paho.mqtt.client as mqtt
import time

temperature = 20
def on_message(client, userdata, message):
    global temperature
    print(f"received message: {str(message.payload.decode('utf8'))}")
    if str(message.payload.decode('utf8')) == "UP":
        temperature += 1
    if str(message.payload.decode('utf8')) == "DOWN":
        temperature -= 1
    print(f"New temperature: {temperature}")
    

mqttBroker = "broker.hivemq.com"

client = mqtt.Client("Smartphone")
client.connect(mqttBroker)

client.loop_start()
print(f"Temperature is {temperature}")
print("Waiting for messages...")

client.subscribe("TEMPCONTROL")
client.on_message=on_message

time.sleep(30)
client.loop_stop()