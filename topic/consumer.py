import sys, os
import CONSTANTS
import pika


cridential = pika.PlainCredentials(username = CONSTANTS.username, password = CONSTANTS.password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host = CONSTANTS.host, 
                                                            port = CONSTANTS.port, 
                                                            virtual_host = CONSTANTS.virtual_host, 
                                                            credentials = cridential))


def receive_msg(queue_name, binding_key):
    def call_back(channel, method, properties, message):
        print(f"received message: {message}")

    # for routing_key in [CONSTANTS.routing_key_info, CONSTANTS.routing_key_warn, CONSTANTS.routing_key_error]:
    channel = connection.channel()
    channel.exchange_declare(exchange = CONSTANTS.exchange_name, exchange_type = CONSTANTS.exchange_type)
    channel.queue_declare(queue = queue_name, durable = True, exclusive = False, auto_delete = False, arguments = None) # 是否排他，即是否私有的，如果为true,会对当前队列加锁，其他的通道不能访问，并且连接自动关闭
    channel.queue_bind(exchange = CONSTANTS.exchange_name, routing_key = binding_key, queue = queue_name) # 将queue绑定到交换机
    
    channel.basic_consume(queue = queue_name, on_message_callback = call_back, auto_ack = True) #收到消息就删除
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("ctrl + c pressed")
        channel.stop_consuming()
        

def main():
    queue_name = input("input consumer's queue name(coffee, milktea, juice)：")
    queue_name_to_binding_key_dict = {CONSTANTS.queue_name_coffee: CONSTANTS.binding_key_kafei, 
                                    CONSTANTS.queue_name_milktea: CONSTANTS.binding_key_naicha,
                                    CONSTANTS.queue_name_juice: CONSTANTS.binding_key_guozhi}
    print("receiving message! (ctrl + c to stop)")
    receive_msg(queue_name = queue_name, binding_key = queue_name_to_binding_key_dict[queue_name])
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