# Websocket-mwe
A server produces a random `Gauss(0,1)` each second. The client listens to,
cache the number in-memory and logs the result.

Based on [websockets](https://github.com/python-websockets/websockets) Python's package.

#### Methods
* `synchro`: a synchronous client that listens to the server, consumes
and then goes back to listening to the incoming data in this 
precise order.
* `asyncio`: an asynchronous client that cooperatively listens to the
server and consumes.
* `multithreading`: TBI
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

In case of the `multiprocess` method with RabbitMQ, type in also
```bash
sudo systemctl start rabbitmq ??
export BROKER_HOST=127.0.0.1
python -m client_multiprocess.listener.listener
```

#### On Docker
```bash
docker-compose --profile <method> up --build
```
