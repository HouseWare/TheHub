#!/usr/bin/env python3

# HouseWare
# Jeffrey Kuan
# 3/15/14

# Packages/modules
from package import Package
##from sqlalchemy import *
import time
import threading
import queue
import bridge

# Event handler class
# A logic unit that communicates with devices and other units of the hub including the web server and database by processing messages as necessary
class Event_Handler(inbox, devices):
	running = 1;

# Class constructor
# Parameter(s): a queue of messages and an array of devices
def __init__(self, inbox, devices)
	self.inbox = inbox
	self.devices = devices

# Main run method
# Parameter(s): n/a
def run(self)
	# Event loop
	while running:
		# Time delay
		start = time.clock()
		##Call refresh device method
		
		# Queue check
		while (time.clock() < (start + 60)):
			__pop()

# Queue push method
# Parameter(s): a message to be pushed onto the queue
def push(self, message)
	inbox.put(message)

# Queue pop method
# Parameter(s): n/a
def __pop(self)
	# Empty queue
	if inbox.empty():
		pass
	else:
		message = inbox.get()
		# Data update received
		if :
			##Write to database
		# Refresh request received
		elif :
			##Call refresh device method
		# Termination signal received
		else:
			running = 0

# Class destructor
# Parameter(s): n/a
def __del__(self):
	# Send confirmation message to main control queue
	pass
