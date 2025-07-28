# A micro-service architecture for concurrent requests via different protocols

* A server produces a random `Gauss(0,1)` at the chosen period.
* Requests can be made to HTTP and Websocket endpoints.
* The client listens to, caches the number in-memory and logs the result.
* Clients are implemented in different synchronus and/or concurrent _methods_.

### Methods
* `synchro`: a synchronous client that listens to the server, consumes
and then goes back to listening to the incoming data in this 
precise order.
* `asyncio`: an asynchronous client that listens to the server and consumes in a cooperative way. 
* `multithreading`: implemented with the help of the `concurrent.futures` library
* `multiprocess`: `listener` and `consumer` processes communicating via a message broker, e.g. RabbitMQ.

## How to run

#### Locally
```bash
pip install -r requirements.txt
export WS_PORT=12345
export SERVER_PERIOD=0.5
python -m server.server
```
and in another terminal session
```bash
export WS_HOST=127.0.0.1
export WS_PORT=12345
export LISTENER_PERIOD=1
export CONSUMER_PERIOD=1
export LOGLEVEL="INFO" # or DEBUG if you wanna delve/drow/die into it
python -m client_<method>.client
```

In case of the `multiprocess` method with RabbitMQ (see section below), type in also
```bash
export BROKER_HOST=127.0.0.1
python -m client_multiprocess.listener.listener
python -m client_multiprocess.consumer.consumer
```

#### On Docker
```bash
docker compose --profile <method> up --build
```

### Setup RabbitMQ for multiprocessing
On a Linux machine
```bash
sudo apt update
sudo apt install rabbitmq-server
```

Once installed the application should automatically serving at port `5672`. Check it by
```bash
sudo ps aux | grep rabbitmq
sudo ss -tnulp | grep 5672 
``` 

To inspect a queue directly from the cli, enable the administration plugin
```bash
sudo rabbitmq-plugins enable rabbitmq_management
```

Then to see messages in a queue
```bash
rabbitmqadmin get queue=<queue-name> count=<N>
```
