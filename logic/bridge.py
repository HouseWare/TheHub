#!/usr/bin/env python

import sys
import pika
import time
import serial
import json
import Queue
import threading

package_name = str(sys.argv[1])

running = True

to_hw = Queue.Queue()
from_hw = Queue.Queue()

credentials = pika.PlainCredentials('hub', 'HubWub!')

connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost',
        5672,
        '/',
        credentials))

channel = connection.channel()

print ' [*] Waiting for messages. To exit press CTRL+C'

def broadcast_callback(ch, method, properties, body):
    print " [x] Received message from broadcast: %r" % (body,)
    if (str(body) == 'kill'):
        running = False
    else:
        to_hw.put_nowait(body)

def package_callback(ch, method, properties, body):
    print " [x] Received message for package: %r" % (body,)
    if (str(body) == 'kill'):
        running = False
    else:
        to_hw.put_nowait(body)

channel.basic_consume(broadcast_callback,
                      queue='package.bcast',
                      no_ack=True)

channel.basic_consume(package_callback,
                      queue='package.' + package_name,
                      no_ack=True)

rabbit = threading.Thread(target=channel.start_consuming)

rabbit.start()
print " [*] RabbitMQ thread initiated."

package = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
print " [*] Serial connection with hardware established."

print " [*] Entering main loop."
while running:

    if (not(to_hw.empty())):
        msg = str(to_hw.get_nowait())
        package.write(msg)
        print " [*] Wrote message to hardware: " + msg

    hw_msg = str(package.readline())
    if (hw_msg != ""):
        from_hw.put_nowait(hw_msg)

    if (not(from_hw.empty())):
        message =  str(from_hw.get_nowait())
        print " [x] Got message from hardware: " + message
        channel.basic_publish(exchange='hub',
            routing_key='logic.package.' + package_name,
            body=message)

package.close()
channel.close()
connection.close()
del rabbit
print ' [*] Thread object deleted. Connections closed.'
