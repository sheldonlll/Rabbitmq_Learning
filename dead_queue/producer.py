import sys, os, time
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


def main():
    channel = connection.channel()
    message = "to dead queue"
    for i in range(10):
        time.sleep(1)
        channel.basic_publish(exchange = CONSTANTS.normal_exchange, routing_key = CONSTANTS.normal_exchange_queue_binding_key, 
                              properties=pika.BasicProperties(expiration="10000"),
                              body = str(i + 1) + " " + message)

    print("send success")
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