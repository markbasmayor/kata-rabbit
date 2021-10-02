#!/usr/bin/env python
import pika
import time

def printer(ch, method, properties, body):
    print("Received: %r" % body.decode())
    time.sleep(body.count(b'.'))
    print("✅ Done")



connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# we need to grab the result here, so that we can get the queue name

channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=printer)


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


connection.close()

