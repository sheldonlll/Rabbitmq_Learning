import queue
import sys, os
import CONSTANTS
import pika


cridential = pika.PlainCredentials(username = CONSTANTS.username, password = CONSTANTS.password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host = CONSTANTS.host, 
                                                            port = CONSTANTS.port, 
                                                            virtual_host = CONSTANTS.virtual_host, 
                                                            credentials = cridential))


def main():
    channel = connection.channel()
    channel.exchange_declare(exchange = CONSTANTS.exchange_name, exchange_type = CONSTANTS.exchange_type)

    for i in range(20):
        message = "hello {}".format(i + 1)
        channel.basic_publish(exchange = CONSTANTS.exchange_name, queue = "worker-queue", body = message)

    print("send success")

    channel.close()
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