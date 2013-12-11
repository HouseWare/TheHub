#!/usr/bin/env python

import sys
import pika
import serial
import Queue
import threading

# get the name of the package from program arguments
package_name = str(sys.argv[1])

# how we know whether we're done (hint, we're not done yet)
running = True

# thread-safe queues to hold messages
to_hw = Queue.Queue()
from_hw = Queue.Queue()

# credentials for access to the RabbitMQ server
credentials = pika.PlainCredentials('hub', 'HubWub!')

# the connection to use for asynchronous callbacks
callback_connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost',
        5672,
        '/',
        credentials))

# the connection we'll use to publish messages on
publish_connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost',
        5672,
        '/',
        credentials))

# setup both our callback channel and our publishing channel using connections
callback_channel = callback_connection.channel()
publish_channel = publish_connection.channel()

def broadcast_callback(ch, method, properties, body):
    # if we get a kill message then stop consuming on the channel
    if (str(body) == 'kill'):
        callback_channel.stop_consuming()
   
    # place the message into the 'To Hardware' queue 
    to_hw.put_nowait(body)

def package_callback(ch, method, properties, body):
    # if we get a kill message then stop consuming on the channel
    if (str(body) == 'kill'):
        callback_channel.stop_consuming()
   
    # place the message into the 'To Hardware' queue 
    to_hw.put_nowait(body)

# assign broadcast_callback to consumer for package.bcast
callback_channel.basic_consume(broadcast_callback,
                      queue='package.bcast',
                      no_ack=True)

# assign package_callback to consumer for package.<insert name here>
callback_channel.basic_consume(package_callback,
                      queue='package.' + package_name,
                      no_ack=True)

# create a new thread object to start consuming on the callback channel
rabbit = threading.Thread(target=callback_channel.start_consuming)

# start the thread
rabbit.start()

# establish serial connection with hardware. reads timeout in 1 second
package = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# main loop
while running:

    if (not(to_hw.empty())):
        
        # pull a message off the 'To Hardware' queue
        msg = str(to_hw.get_nowait())

        if (msg == 'kill'):
            # welp, looks like we're done now
            running = False
        else:
            # send the message off to the hardware over serial            
            package.write(msg)

    # read a message from hardware. susceptible to 1 second timeout 
    hw_msg = str(package.readline())

    if (hw_msg != ""):
        # place the non-blank message into the 'From Hardware' queue
        from_hw.put_nowait(hw_msg)

    if (not(from_hw.empty())):

        # cast the message as a string, publish it to the 'From Hardware' queue 
        message =  str(from_hw.get_nowait())
        publish_channel.basic_publish(exchange='hub',
            routing_key='logic.package.' + package_name,
            body=message)

# shut down all the connections and get outta dodge
package.close()
publish_channel.close()
callback_connection.close()
publish_connection.close()

# delete the thread object, just in case
del rabbit
