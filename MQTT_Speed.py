'''
@created By 
Ashwini Kulkarni

Project IOT Clould
Data Streaming using MQTT to IBM Blumix Device

Data {
"Speed_limit":Speed_limit for specific road, 
"Act_Speed": Act_DatSpeed of a vehicle, 
"plate_no":  reg No of vehicle
	
}

'''

import time
import paho.mqtt.client as mqtt
import json
import uuid
import datetime
import random
import string

def is_positive(reading):
	if reading < 0:
		return (reading * -1)
	else:
		return reading
	
	
def get_plate():
			plate_format = "LLNN LLL"
			plate = []
			for i in plate_format:
				if i == 'L':
					plate.append(random.choice(string.ascii_letters[26:]))
				elif i == 'N':
					plate.append(str(random.randint(0, 9)))
				else :
					plate.append(i)
			#self.no_plate_idle = plate	
			return 	" ".join(plate)
			

#Class for retrieving CPU % utilisation
class Device1(object):
		def __init__(self):
				self.speed_idle = 0
				self.act_speed_idle = 0
				self.no_plate_idle = []
				
				self.list= [20,30,40,60,80]
		def get_act_speed(self):
				self.act_speed_idle = random.randrange((self.speed_idle-30),self.speed_idle+30,10)
				return self.act_speed_idle
		
		def get_speed(self):
				self.speed_idle = random.choice(self.list)
				return self.speed_idle
		
		def get_plate(self):
			plate_format = "LLNN LLL"
			plate = []
			for i in plate_format:
				if i == 'L':
					plate.append(random.choice(string.ascii_letters[26:]))
				elif i == 'N':
					plate.append(str(random.randint(0, 9)))
				else :
					plate.append(i)
			self.no_plate_idle = plate	
			return 	self.no_plate_idle

		

#Initialise class to retrieve CPU Usage
Device1 = Device1()

#Set the variables for connecting to the iot service
broker = ""
#topic = "Iot-2/evt/my2Event/fmt/json"
topic = "iot-2/evt/myEvent/fmt/json"
username = "use-token-auth"
password = "12345678"  #auth-token
organization = "p9u631"                   #org_id
deviceType = "Speed_Device"

#topic = "iot-2/evt/status/fmt/json"


#Creating the client connection
#Set clientID and broker
clientID = "d:" + organization + ":" + deviceType + ":" + "speed_device_act"
broker = organization + ".messaging.internetofthings.ibmcloud.com"
mqttc = mqtt.Client(clientID)

#Set authentication values, if connecting to registered service
if username is not "":
		mqttc.username_pw_set(username, password=password)

mqttc.connect(host=broker, port=1883, keepalive=60)


#Publishing to IBM Internet of Things Foundation
mqttc.loop_start() 

while mqttc.loop() == 0:
	
		Speed_limit = Device1.get_speed()
		Act_Speed =is_positive(Device1.get_act_speed())
		plate_no =str(get_plate())
		print Speed_limit
		print Act_Speed
		print plate_no

		msg = json.JSONEncoder().encode({"d":{"Speed_limit":Speed_limit, "Act_Speed": Act_Speed, "plate_no": plate_no}})
		
		mqttc.publish(topic, payload=msg, qos=0, retain=False)
		print "message published"

		time.sleep(5)
		pass


