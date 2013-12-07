#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()

channel.basic_publish(exchange='hub',
                      routing_key='logic.package.test',
                      body=sys.argv[1])
print " [x] Sent %r" % (sys.argv[1])

connection.close()
