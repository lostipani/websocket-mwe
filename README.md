# Websocket-mwe
A server produces a random Gauss(0,1) each second. The client listens to, cache the number and compute mean and std of the sequence so far.

Based on [websockets](https://github.com/python-websockets/websockets) Python's package.

## How to run

#### Locally
```bash
pip install -r requirements.txt
python server/server.py
```
and in another terminal session
```bash
export WS_HOST="127.0.0.1"
export WS_PORT=12345
export LOGLEVEL="INFO"
python client/client.py
```

#### On Docker
```bash
docker-compose up --build -d
docker logs websocket-mwe-client-1 --follow
```
