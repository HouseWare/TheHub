#HouseWare

#Event loop
#Regularly queries the module, updates the database, and checks the queues

#!/usr/bin/env python

# Libraries
import pika
from package import Package
import time
import threading
from subprocess import Popen
import queue
import logging

inbox = queue.Queue()

'''
# RabbitMQ conenction info:
credentials = pika.PlainCredentials('hub', 'HubWub!')
callback_connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost',
        5672,
        '/',
        credentials))
callback_channel = callback_connection.channel()

bcast_connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost',
        5672,
        '/',
        credentials))
bcast_channel = bcast_connection.channel()
'''

# Database Service creation:

# Get existing packages from database:
# TODO: Actually use db service to get package information
packages = []

# In a loop, get each package and spin off it's bridge.
pckg = Package('cf412')
pckg.id = 1 #pckg.id = db_service.###
pckg.pid = 1000 # pckg.id = return pid from starting process.
packages.append(pckg)

running = True

# Starting package bridges:
bridge_process = Popen(["./bridge.py", "demo"])

print ' [*] Waiting for messages. To exit press CTRL+C'

def package_callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

def web_callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    if(body == 'kill'):
        callback_channel.basic_publish(exchange = 'hub', routing_key = 'package.bcast', body = 'kill')
        callback_channel.stop_consuming()
	event_queue.put_nowait('kill')

callback_channel.basic_consume(package_callback,
                      queue='logic.package',
                      no_ack=True)

callback_channel.basic_consume(web_callback,
                      queue='logic.web',
                      no_ack=True)

'''
print "Starting Rabbit Response thread..."
event_handler = threading.Thread(target = callback_channel.start_consuming)
event_handler.start()
'''

print "Initializing main event loop..."

while True:
    time.sleep(1)
    print("Hello, World!")

    bcast_channel.basic_publish(exchange = 'hub', routing_key = 'package.bcast', body = '{"req":04}')
    bcast_channel.basic_publish(exchange = 'hub', routing_key = 'package.bcast', body = '{"req":50}')
    bcast_channel.basic_publish(exchange = 'hub', routing_key = 'package.bcast', body = '{"req":51}')
    bcast_channel.basic_publish(exchange = 'hub', routing_key = 'package.bcast', body = '{"req":52}')

    if (not(event_queue.empty())):
	running = False

print "Terminating main event loop..."

print "Waiting for thread to finish"
while (event_handler.is_alive()):
    print 'waiting..'
    time.sleep(.5)

callback_channel.close()
bcast_channel.close()
callback_connection.close()
bcast_connection.close()

