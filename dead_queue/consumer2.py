from enum import auto
import sys, os
from multiprocessing import Process
import CONSTANTS
import pika


try:
    cridential = pika.PlainCredentials(username = CONSTANTS.username, password = CONSTANTS.password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host = CONSTANTS.host, 
                                                            port = CONSTANTS.port, 
                                                            virtual_host = CONSTANTS.virtual_host, 
                                                            credentials = cridential))
except Exception as e:
    print("error occured when connect to rabbitmq!")
    print("docker pull rabbitmq:management \n\
docker run -di --name myrabbit -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin -p 15672:15672 -p 5672:5672 -p 25672:25672 -p 61613:61613 -p 1883:1883 rabbitmq:management \n\
open http://YourIP:15672\n\
change CONSTANTS.py's host, username, password")



def receive_msg(queue_name):
    channel = connection.channel()

    channel.exchange_declare(exchange = CONSTANTS.dead_exchange, exchange_type = CONSTANTS.dead_exchange_type, durable = True,
                             auto_delete = False, arguments = None)
    channel.queue_declare(queue = CONSTANTS.dead_queue, durable = False, exclusive = False, auto_delete = False, arguments = None)
    channel.queue_bind(queue = CONSTANTS.dead_queue, exchange = CONSTANTS.dead_exchange, routing_key = CONSTANTS.dead_exchange_queue_binding_key)

    def call_back(channel, method_frame, properties, message):
        print(f"consumer2-received message: {message}")

    channel.basic_consume(queue = queue_name, on_message_callback = call_back, auto_ack = True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("ctrl + c pressed")
        channel.stop_consuming()


def main():
    receive_msg(queue_name = CONSTANTS.dead_queue)
    connection.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("ctrl + c pressed")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)