#!/usr/bin/env python3

"""
HouseWare
Jeffrey Kuan
6/3/14
"""

# Imports
import time
import threading
import queue
import bridge
from ..database import db

# Event handler class
# A logic unit class that communicates with devices, the web server, and the database by applying logic to messages as necessary
class EventHandler:
    running = True

    door_open_value = 1
    temp_high_value   = 63
    light_on_value  = 511

    # Class constructor
    # Parameter(s): a queue for messages and an array of devices
    def __init__(self, inbox, devices):
        self.inbox = inbox
        self.devices = devices

    # Main run method
    # Parameter(s): n/a
    def run(self):

        # Main event loop
        while running:
            start = time.clock()    # Starts time delay
            self.refresh()

            # Check queue for messages
            while time.clock() < (start + 60):
                self.pop()

    # Queue push method
    # Parameter(s): a message to be pushed onto the queue
    def push(self, message):
        inbox.put(message)

    # Queue pop method
    # Parameter(s): n/a
    def pop(self):

        # No messages
        if inbox.empty():
            pass

        # Messages found
        else:
            message = inbox.get()

            # Sensor update received
            if not isinstance(message, str):
               self.write(message)

            # Other message received
            else:

                # Refresh request received
                if message == 'refresh':
                    self.refresh()

                # Termination signal received
                else:   
                    running = False

    # Request refreshed sensor values
    # Parameter(s): n/a
    def refresh(self):

        # Send message to each device
        for x in devices:
            x.send_message("refresh")

    # Write sensor values to database and apply logic if necessary
    # Parameter(s): a database statement
    def write(self, message):

        # Pass to database
        db.session.add_all([message])
        db.session.commit()

        # Door logic
        if (isinstance(message.sensor, wired_door_sensor) or isinstance(message.sensor, wireless_door_sensor)):

            # Door open
            if message.sensor.value == door_open_value:
                door_notification = db.Notification(read = False, value = "The door is open!", severity = notification)
                db.session.add_all([door_notification])
                db.session.commit()

        # Temperature logic
        if (isinstance(message.sensor, wired_temp_sensor) or isinstance(message.sensor, wireless_temp_sensor)):

            # Temperature high
            if message.value > temp_high_value
                temp_notification = db.Notification(read = False, value = "The temperature is over 9000!", severity = notification)
                db.session.add_all([temp_notification)
                db.session.commit()

        # Light logic
        if (isinstance(message.sensor, wired_light_sensor) or isinstance(message.sensor, wireless_light_sensor)):

            # Light high
            if message.value > light_on_value:
                light_notification = db.Notification(read = False, value = "The light is on!", severity = notification)
                db.session.add_all([light_notification])
                db.session.commit()

    # Class destructor
    # Parameter(s): n/a
    def __del__(self):
        pass
