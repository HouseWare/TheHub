#!/usr/bin/env python

import pika
import package
import time
import threading
from subprocess import Popen


# RabbitMQ conenction info:
credentials = pika.PlainCredentials('hub', 'HubWub!')
connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost',
        5672,
        '/',
        credentials))
callback_channel = connection.channel()

bcast_connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost',
        5672,
        '/',
        credentials))
bcast_channel = connection.channel()

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


print ' [*] Waiting for messages. To exit press CTRL+C'

def package_callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)


def web_callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)


callback_channel.basic_consume(package_callback,
                      queue='logic.package',
                      no_ack=True)

callback_channel.basic_consume(web_callback,
                      queue='logic.web',
                      no_ack=True)

print "Starting Rabbit Response thread..."
event_handler = threading.Thread(target = callback_channel.start_consuming)
event_handler.start()

print "Starting main event loop..."

while running:
    bcast_channel.basic_publish(exchange = 'hub', routing_key = 'package.bcast', body = '{"req":"04"}'
    bcast_channel.basic_publish(exchange = 'hub', routing_key = 'package.bcast', body = '{"req":"50"}'
    bcast_channel.basic_publish(exchange = 'hub', routing_key = 'package.bcast', body = '{"req":"51"}'
    bcast_channel.basic_publish(exchange = 'hub', routing_key = 'package.bcast', body = '{"req":"52"}'
    time.Sleep(5)

    
