#!/usr/bin/env python

import sys
import time
import serial
import queue
import threading


running = True


class bridge:

		to_hw = queue.Queue()
		from_hw = None
		running = True
		serialport = '/dev/ttyUSB0'
		serialrate = 9600
		myserial = None
		stopped = True
		test = False

		def serialport(self): return self._serialport
		def serialport(self, value):self._serialport = value

		def from_hw(self): return self._from_hw
		def from_hw(self, value):self._from_hw = value

		def __init__(self):
			pass

		def stop(self):
			to_hw.write("kill")


		def start(self):
			print("starting")
			if ((self.from_hw != None) and (self.serialport != None) and (self.serialrate != None) and self.stopped):
				if (self.test):
						mythread = threading.Thread(target=self.theprocess)
						print("starting process")
						mythread.start()
				else:
						self.myserial = serial.Serial(self.serialport, self.serialrate, timeout=1)
						if (self.myserial.isOpen()):
								mythread = threading.Thread(target=self.theprocess)
								mythread.start()
			else:
				#kick and scream
				print("kicking and screaming")
					
		def theprocess(self):
				self.stopped = False
				self.running = True
				while self.running:
					#print ("running=" + str(self.running))
					if (not(self.to_hw.empty())):
						msg = str(self.to_hw.get_nowait())
						if (msg == 'kill'):
							self.running = False
						else:
							if (not(self.test)):
								self.myserial.write(msg)
							print (" [*] Wrote message to hardware: " + msg)
					if (not(self.test)):
						hw_msg = str(self.myserial.readline())
						if (hw_msg != ""):
								self.from_hw.put_nowait(hw_msg)
								print (" [x] Got message from hardware: " + hw_msg)

				if (not(self.test)):		
						self.myserial.close()
				self.stopped = True
