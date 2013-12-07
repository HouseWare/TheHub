#!/usr/bin/env python

import pika

credentials = pika.PlainCredentials('hub', 'HubWub!')

connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost',
        5672,
        '/',
        credentials))

channel = connection.channel()

print ' [*] Waiting for messages. To exit press CTRL+C'

def package_callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

def web_callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

channel.basic_consume(package_callback,
                      queue='logic.package',
                      no_ack=True)

channel.basic_consume(web_callback,
                      queue='logic.web',
                      no_ack=True)

channel.start_consuming()
