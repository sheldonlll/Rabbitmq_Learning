# Rabbitmq_Learning

0. install docker on linux
1. docker pull rabbitmq:management
2. docker run -di --name myrabbit -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin -p 15672:15672 -p 5672:5672 -p 25672:25672 -p 61613:61613 -p 1883:1883 rabbitmq:management
3. open browser: http://YourIP:15672
4. change each subfilefolder's CONSTANTS.py's host to YourIP
5. python .\rabbitmq_learning\\['direct', 'fanout', ..]\consumer.py
6. python .\rabbitmq_learning\\['direct', 'fanout', ..]\producer.py