 ### Packages ###

import grovepi
from time import sleep
import time
import paho.mqtt.client as mqtt_client
import paho.mqtt.subscribe as mqtt_subscribe
# import scripts.display as oled ## thing necessary for the OLED display
import display as oled ## thing necessary for the OLED display

### Packages END ###



### CSV definition ###

# Create output file name
output_filename = 'output/group33&34_measurement_final.csv'

# Create header line (like a header of the table)
header = ("Timestamp", "Set Temperature","Temperature","Humidity","Air Quality") # define array of header values (names of columns)
strHeader = ';'.join(header) # Join all data into one string separated by ; (as required for CSV)

# Write header line to the file 
csv_file = open(output_filename, 'a+') # Open in 'a+' mode, new data is appended to the end of the file
csv_file.write(strHeader + '\n') # Finish the line using '\n' character
csv_file.close() # Closes the file for further operations (and actually writes data to the file)

### CSV definition END ###



### User variables

offline = False # set to True if working offline, as it allows the script to continue even if MQTT cannot connect
client_id = "StudentGroup_33&34"
mqtt_host = "broker.hivemq.com"
mqtt_port = 1883
# Topics need to be adjusted to fit Node-RED Dashboard
# Receive Temperature Instructions: TEMPCONTROL
# Send Temperature Information: TEMPDISPLAY
# publishing_topic1 = "testtopic/7ZW5M0/group_33&34/temperature"
publishing_topic1 = "TEMPDISPLAY"
publishing_topic2 = "testtopic/7ZW5M0/group_33&34/humidity"
publishing_topic3 = "testtopic/7ZW5M0/group_33&34/airquality"
client_topic = "testtopic/7ZW5M0/group_33&34/input"
# subscription_topic = "testtopic/7ZW5M0/group_33&34/subscription"
subscription_topic = "TEMPCONTROL"
num_of_tries_mqtt = 3 #maximum number of tries for MQTT connection

connectedFlag = False # tracks if client is connected
subscribedFlag = False # tracks if client is subscribed to a topic

### User variables END ###



### MQTT protocol functions ###

#MQTT function on_message https://pypi.org/project/paho-mqtt/#subscribe-unsubscribe
def on_message(client, userdata, message):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("Received message '" + str(message.payload) + "' on topic '"
        + message.topic + "' with QoS " + str(message.qos))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

def on_subscribe(client, userdata, mid, granted_qos):
    global subscribedFlag ## Global required in order to be able to make changes
    subscribedFlag = True
    print (client, " subscribed!")

def on_unsubscribe(client, userdata, mid):
    global subscribedFlag
    subscribedFlag = False
    print (client, " unsubscribed!")
    
def on_connect(client, userdata, flags, rc):
    global connectedFlag
    connectedFlag = True
    print(">>>>>>>>>> Sucess! MQTT connected! >>>>>>>>>>>")

def on_disconnect(client, userdata, rc):
    global connectedFlag
    connectedFlag = False
    print(">>>>>>>>>> Attention! MQTT disconnected! >>>>>>>>>>>")
    print(" Trying to reconnect!")
    try_to_connect_and_subscribe(client_id, mqtt_host, mqtt_port, max_num_of_attempts = num_of_tries_mqtt, topic = subscription_topic)




def try_to_connect_and_subscribe(client_id, mqtt_host, mqtt_port, max_num_of_attempts = 1, topic = 'testtopic/#', qos = 2): # Tries to connect to MQTT server # Returns Client class on sucess or FALSE on fail.

    mqtt = False

    while max_num_of_attempts > 0:
        try:
            #print("Trying to connect to MQTT")
            
            #creating MQTT client
            mqtt = mqtt_client.Client(client_id)
            print("DEBUG: Client created!")
            
            mqtt.on_connect = on_connect
            mqtt.on_disconnect = on_disconnect
            mqtt.on_subscribe = on_subscribe
            mqtt.on_unsubscribe = on_unsubscribe
            mqtt.on_message = on_message # define function that executes on message arrival
            #connecting to MQTT server
            
            print("DEBUG: Attempting to connect")
            mqtt.connect(host = mqtt_host, port = mqtt_port)
            print("DEBUG: MQTT connected!")
            
            mqtt.loop_start() #runs the network loop
            global connectedFlag
            connectedFlag = True # sets the connection flag
            
            print("DEBUG: Trying to subscribe to '"+topic+"'")
            mqtt.subscribe(topic, qos) # subscribes to the desired topic
            sleep(3)
            
            return mqtt
            break # exit loop if connection established
        
        except:
            print("MQTT connection error!")
            mqtt = False
            #print("Check your network connectivity and MQTT setings!")
            #exit()
            
        max_num_of_attempts -= 1    
        print("Attempts left: ",max_num_of_attempts)    
        print("--->")
        sleep(5) # 5sec inbetween connection attempts
        
### MQTT protocol functions END ###
        
        
        
### Sensor definitions ###
# Temperature and Humidity sensor
dhtSensor = 2  # The (digital humidity & temperature) Sensor goes on digital port D2.
blue = 0    # The Blue colored sensor.

# Air quality sensor
daqSensor =  0 # The (digital air qualtiy) Sensor goes on digital port A0.
grovepi.pinMode(daqSensor,"INPUT")


# Input potentiometer
dpmSensor = 1 # The (digital potentiometer) Sens goes on digital port A1
grovepi.pinMode(dpmSensor,"INPUT")
sleep (2) # let the board load commands

# Initialize sensors
time.sleep(3*10) # Allow some time for sensor to initialise (first time 3min is recommended)

### Sensor definitions END ###




### Starting main part of the script!
print("### Script Started! ###")

# Trying to connect to MQTT server
if not offline:
    
    mqtt = try_to_connect_and_subscribe(client_id, mqtt_host, mqtt_port, max_num_of_attempts = num_of_tries_mqtt, topic = subscription_topic)
    if mqtt == False:
        print("MQTT connection error!")
        print("Check your network connectivity and MQTT setings!")
        
        if offline:
            print ("Attention! Offline mode activated, script will continue")
        else:
            print ("Attention! Offline mode not activated, script will terminate")
            print(">>> Script Terminating!!!\n \n \n")
            exit() 


# Start time
t0=time.time()

# Activate OLED
display = oled.GroveOledDisplay128x64(bus=1)
# Main loop
i=1
while True:
    
    try:
        print("\n")
        # TIMESTAMP
        timeStamp=time.time()-t0;
        
        # INPUT POTENTIOMETER
        pot = grovepi.analogRead(dpmSensor)
        voltage = round(pot*5/1023 , 2) # convert sensor readout to voltage
        degrees = round(voltage*300/5 , 2) # convert voltage to angle in degrees 0-300
        setTemp = round(15+(15/300)*degrees,1) # convert to a set temperature betweeon 15 and 30 degrees Celsius
        
        # TEMPERATURE & HUMIDITY
        # The first parameter is the port, the second parameter is the type of sensor.
        [temp,humidity] = grovepi.dht(dhtSensor, blue) # Function returns temperature and humidity 
        
        # AIR QUALITY
        airquality = grovepi.analogRead(daqSensor)
        if airquality <50:
            airQ="Low pollution"
        elif airquality <200:
            airQ="Moderate pollution"
        elif airquality <500:
            airQ="High pollution"
        else:
            airQ="Severe pollution"
        
        # Printing readout
        print("Iteration = %.00f \nTime = %.05f s \nSet Temperature = %.00f \N{DEGREE SIGN}C \nTemperature = %.00f \N{DEGREE SIGN}C \nHumidity = %.00f %% \nAir quality = %s " % (i,timeStamp, setTemp, temp, humidity, airQ))
        client_msg_0 = setTemp
        msg_1 = temp
        msg_2 = humidity
        msg_3 = airquality
        i=i+1
        
        # Printing to OLED
        display.set_cursor(0, 0)
        display.puts('Time= '+str(round(timeStamp,2))+' s        ')
        display.set_cursor(1,0)
        display.puts('Set Temp= '+str(round(setTemp,0))+' C         ')
        display.set_cursor(2, 0)
        display.puts('Temp= '+str(temp)+' C             ')
        display.set_cursor(3,0)
        display.puts('Humid= '+str(humidity)+' %                 ')
        display.set_cursor(4,0)
        display.puts('Air qual= '+str(airquality)+' ppm                ')
      
        if connectedFlag:
#                 print("DEBUG: Trying to publish message!")
                mqtt.publish(topic = publishing_topic1,
                            payload = msg_1,
                            qos=2
                            )
                mqtt.publish(topic = publishing_topic2,
                            payload = msg_2,
                            qos=2
                            )
                mqtt.publish(topic = publishing_topic3,
                            payload = msg_3,
                            qos=2
                            )
                mqtt.publish(topic = client_topic,
                             payload = client_msg_0,
                             qos=2
                             )
                
        
        # CSV writing                
        # Format time, temperature, humidity
        data = [str(timeStamp), str(setTemp), str(temp), str(humidity), str(airquality)]
        strData = ';'.join(data) # Join all data into one string separated by ; (as required for CSV)

        # Write sensor values to the csv file
        csv_file = open(output_filename, 'a+') # Again open (the same) file in 'a+' mode
        csv_file.write(strData + '\n') # Write string of joined (; separated) data & finish the line using '\n' 
        csv_file.close() # Close the file again

        # SMART device real-time intelligence
        print("\nADVISE BY SMART DEVICE: \n")
        if temp-setTemp<-1:
            print("It is getting cold in here! I will turn on heating!")
        elif abs(setTemp-temp)<=1:
            print("Temperature okay!")
        else:
            print("Temperature too high! I will turn on the ventilator.")
            
        if humidity<=60 and humidity>=40:
            print("Humidity is okay!")
        elif humidity<40:
            print("Turning on humidifier!")
        else:
            print("Humidity is too high. I suggest opening a window.")
        
        if airquality <50:
            print("Air quality is okay!")
        elif airquality <200:
            print("The air is a little polluted,I will turn on the ventilator")
        elif airquality <500:
            print("The air is polluted! Open a window!")
        else:
            print("DANGER! The air is severely polluted! EXIT the building IMMEDIATELY")

    except:
        print ("Error occured! (script is continuing)")
    
    sleep (20) # wait 2sec before next readout

print('Stopping loop')
mqtt.loop_stop() #stops the network loop 
