# Websocket-mwe
A server produces a random `Gauss(0,1)` each second. The client listens to,
cache the number in-memory and compute mean and std of the sequence so far.

Based on [websockets](https://github.com/python-websockets/websockets) Python's package.

#### Methods
* `synchro`: a synchronous client that listens to the server, computes
the statistics and then goes back to listening to the incoming data.
* `cooperative`: an asynchronous client that cooperatively listens to the
server and computes the statistics.
* `multithreading`: TBI
* `multiprocessing`: TBI via a bus service

## How to run

#### Locally
```bash
pip install -r requirements.txt
export SERVER_FREQUENCY=0.5
python server/server.py
```
and in another terminal session
```bash
export WS_HOST=127.0.0.1
export WS_PORT=12345
export LOGLEVEL="INFO"
python -m client_<method>.client
```

#### On Docker
```bash
docker-compose --profile <method> up --build
```
