#!/usr/bin/env python


print_messages = True

import sys
import time
import serial
import queue
import threading
import re
import ../database/db



class Bridge():

	
		def __init__(self, from_hw_queue, device):

			self.device = device;

			#self.device_id = device_id
			#self.sensor_ids = sensor_ids#{"A1".."AZ","D1".."DZ"}, list of sensor IDs as outlined in protocol

			self.from_hw = from_hw_queue
			
			self.to_hw = queue.Queue()
			self.running = True
			self.serialport = '/dev/ttyUSB0'
			self.serialrate = 9600
			self.myserial = None
			self.stopped = True
			self.test = False
			
			if test:
				self.fromhwtest = queue.Queue()

		#stop, send the kill message to the thread
		def stop(self):
			self.to_hw.put_nowait("kill")


		def start(self):
			print("starting")
			#check that required information is set
			if ((self.from_hw != None) and (self.serialport != None) and (self.serialrate != None) and self.stopped):
				if (self.test):#testing
						mythread = threading.Thread(target=self.theprocess)
						if print_messages:
							print("starting process")
						mythread.start()
				else:
						#setup serial and start thread
						self.myserial = serial.Serial(self.serialport, self.serialrate, timeout=1)
						if (self.myserial.isOpen()):
								mythread = threading.Thread(target=self.theprocess)
								mythread.start()
			else:
				#kick and scream
				
				if (self.from_hw == None):
					print("from Hardware queue not yet set")
				if (self.serialport == None):
					print("Serial Port not set")
				if (self.serialrate == None):
					print("Serial Rate not set")
				if not(self.stopped):
					print("Already running");
					
		
					
		def theprocess(self):
				self.stopped = False
				self.running = True
				while self.running:
										
					#message for hardware
					if (not(self.to_hw.empty())):
						msg = str(self.to_hw.get_nowait())
						if (msg == 'kill'):
							self.running = False
							if print_messages:
								print(" Got a kill command")
						else:
							if (not(self.test)):
								self.myserial.write(msg)
							if print_messages:
								print (" [*] Wrote message to hardware: " + msg)
							
							
					if (not(self.test)):#not a test
						hw_msg = str(self.myserial.readline())						
						if (hw_msg != ""):#got a message from the hardward
								if print_messages:
									print (" [x] Got message from hardware: " + hw_msg)
								self.from_hw.put_nowait(self.translate_message_fromhw(hw_msg))
								if print_messages:
									print (" [x] Translated message from hardware: " + self.translate_message_fromhw(hw_msg))
								
					else:#is a test
						if (not( self.fromhwtest.empty())):
							hw_msg = self.fromhwtest.get()			
							if print_messages:				
								print (" [x] Got test message from hardware: " + hw_msg)
							self.from_hw.put_nowait(self.translate_message_fromhw(hw_msg))					
							

				if (not(self.test)):#not a test, clean up
						self.myserial.close()
				self.stopped = True
				
				
		def send_message(self, themessage):
			#translated_message = translate_message_tohw(themessage)
			if print_messages:
				print (" [x] Got message to pass to hardware: " + themessage)
			
			if themessage == "kill":
				to_hw.to_hw.put_nowait("kill")
			else:
				#default behavior get all
				for somesensor in device.sensors
				
					if re.match("[A-Z][A-Z0-9]",sensor.id):
						self.to_hw.put_nowait(sensor.id);
					else:
						print("Bad sensor ID: "+sensor.id)
				
				
#				for sensor in self.sensor_ids:
#					if re.match("[A-Z][A-Z0-9]",sensor):
#						self.to_hw.put_nowait(sensor);
#					else:
#						print("Bad sensor ID: "+sensor)
		
		
		#place holding for message translation
		def translate_message_tohw (themessage):
			#do some translating eventually
			outmessage = themessage
			return outmessage

		def translate_message_fromhw (self,themessage):
			#do some translating			
			if themessage[0] == "V":
				
				#get appropriate sensor object
				thesensor = db.session.query(db.Sensor).filter(db.Sensor.device_id==mydevice.id).filter(db.Sensor.pin=themessage[1:3]).all()[0]
				
				#create dataeven object and return
				outmessage = db.DataEvent(device = self.device, sensor = thesensor, value = int(themessage[3:6]))
				
			return outmessage
