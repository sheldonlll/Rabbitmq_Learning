# Rabbitmq_Learning

0. install docker on linux
1. docker pull rabbitmq:management
2. docker run -di --name myrabbit -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin -p 15672:15672 -p 5672:5672 -p 25672:25672 -p 61613:61613 -p 1883:1883 rabbitmq:management
3. open browser: http://YourIP:15672
4. change each subfilefolder's CONSTANTS.py's host to YourIP
5. - python .\rabbitmq_learning\\['direct', 'fanout', 'topic']\\consumer.py
   - python .\rabbitmq_learning\\['direct', 'fanout', 'topic']\\producer.py

6. - python .\rabbitmq_learning\worker\\['fair', 'pooling']\\producer.py
   - python .\rabbitmq_learning\worker\\['fair', 'pooling']\\consumer1.py
   - python .\rabbitmq_learning\worker\\['fair', 'pooling']\\consumer2.py

7. - python .\rabbitmq_learning\dead_queue\consumer1.py
   - ctrl + c to stop consumer1
   - python .\rabbitmq_learning\dead_queue\producer.py # producer已发送10条消息，此时normal queue中有10条未消费消息, 时间过去10秒，正常队列中的消息由于没被消费，进入dead queue
   - python .\rabbitmq_learning\dead_queue\consumer2.py