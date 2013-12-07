#!/usr/bin/env python

import time
import pika

credentials = pika.PlainCredentials('hub', 'HubWub!')

connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost',
        5672,
        '/',
        credentials))

channel = connection.channel()

while True:

    channel.basic_publish(exchange='hub',
                      routing_key='package.bcast',
                      body='Hello World!')

    #print " [x] Sent 'Hello World!'"

    time.sleep(30)    

connection.close()
