#!/usr/bin/env python
import pika
import time

def printer(ch, method, properties, body):
    print("Received: %r" % body.decode())
    time.sleep(body.count(b'.'))
    print("✅ Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)



connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# This is redundant, but is considered a good practice in case the consumer
# runs before the producer or before the queue is created.
# The method itself is idempotent and won't create a new queue if one already exists.
channel.queue_declare(queue='tasks', durable=True)

channel.basic_consume(queue='tasks',
                      on_message_callback=printer)


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


connection.close()

