#!/usr/bin/env python
import pika
import sys


message = ' '.join(sys.argv[1:]) or "Hello World!"

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='tasks', durable=True)

channel.basic_publish(exchange='',
                      routing_key='tasks',
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ),
                      body=message)

connection.close()

