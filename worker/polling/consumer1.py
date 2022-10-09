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
    print("connect to rabbitmq error occured!")
    print("docker pull rabbitmq:management \n\
           docker run -di --name myrabbit -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin -p 15672:15672 -p 5672:5672 -p 25672:25672 -p 61613:61613 -p 1883:1883 rabbitmq:management \n\
           open http://YourIP:15672\n\
           change CONSTANTS.py's host, username, password")


def receive_msg(queue_name):
    channel = connection.channel()
    channel.basic_qos(prefetch_count = 1) # 每次只消费一个消息
    channel.queue_declare(queue = queue_name, durable = True, exclusive = False, auto_delete = False, arguments = None) # 是否排他，即是否私有的，如果为true,会对当前队列加锁，其他的通道不能访问，并且连接自动关闭

    def call_back(channel, method_frame, properties, message):
        for _ in range(999999): pass # 模拟worker queue延时
        print(f"consumer1-received message: {message}")
        #delivery_tag: 确认队列中哪个具体消息，multiple：是否开启多个消息同时确认
        channel.basic_ack(delivery_tag = method_frame.delivery_tag, multiple = False)


    #关闭消息确认
    channel.basic_consume(queue = queue_name, on_message_callback = call_back, auto_ack = False)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("ctrl + c pressed")
        channel.stop_consuming()


def main():
    receive_msg(queue_name = "worker")
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