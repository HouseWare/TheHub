#!/usr/bin/env python3

"""
HouseWare
Jeffrey Kuan
4/22/14
"""

# Imports
import time
import threading
import queue
import bridge
from ..database import db

# Event handler class
# A logic unit class that communicates with devices, the web server, and the database by applying logic to messages as necessary
class EventHandler(inbox, devices):
    running = True;


# Class constructor
# Parameter(s): a queue for messages and an array of devices
def __init__(self, inbox, devices)
    self.inbox = inbox
    self.devices = devices

    # Main run method
    # Parameter(s): n/a
    def run(self)

        # Main event loop
        while running:
            start = time.clock()    # Starts time delay
            refresh()

            # Check queue for messages
            while time.clock() < (start + 60):
                pop()

    # Queue push method
    # Parameter(s): a message to be pushed onto the queue
    def push(self, message)
        inbox.put(message)

    # Queue pop method
    # Parameter(s): n/a
    def pop(self)

        # No messages
        if inbox.empty():
            pass

        # Messages found
        else:
            message = inbox.get()

            # Data update received
            if """""":
               write(message)

            # Refresh request received
            elif """""":
                refresh()

            # Termination signal received
            else:   
                running = False

    # Request refreshed sensor values
    # Parameter(s): n/a
    def refresh(self)

        # Send message to each device
        for x in devices:
            x.send_message("refresh")

    # Write sensor values to database and apply logic if necessary
    # Parameter(s): a database statement
    def write(self, message)
        """""""

    # Class destructor
    # Parameter(s): n/a
    def __del__(self)
        pass
