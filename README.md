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
* `multiprocessing`: TBI via a bus service

## How to run

#### Locally
```bash
pip install -r requirements.txt
export SERVER_PERIOD=0.5
python server/server.py
```
and in another terminal session
```bash
export WS_HOST=127.0.0.1
export WS_PORT=12345
export LOGLEVEL="INFO" # or DEBUG if you wanna delve/drow/die into it
python -m client_<method>.client
```

#### On Docker
```bash
docker-compose --profile <method> up --build
```
