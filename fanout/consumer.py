#!/usr/bin/env python
import pika
import time

def printer(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    time.sleep(body.count(b'.'))
    print(" [x] Done")



connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# we need to grab the result here, so that we can get the queue name
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)

channel.basic_consume(queue=queue_name,
                      auto_ack=True,
                      on_message_callback=printer)


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


connection.close()

