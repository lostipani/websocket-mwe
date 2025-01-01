import os
from typing import Dict
import random
import asyncio

import uvicorn
from fastapi import FastAPI, WebSocket, status
from fastapi.websockets import WebSocketDisconnect

app = FastAPI()


def producer() -> Dict[str, float]:
    return {"value": random.gauss(0, 1)}


@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = producer()
        try:
            await websocket.send_json(data)
        except WebSocketDisconnect:
            break
        await asyncio.sleep(1)


@app.get("/http")
def http_endpoint():
    return producer()


@app.get(
    "/healthcheck",
    status_code=status.HTTP_200_OK,
)
def healthcheck():
    return {"value": "OK"}


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=int(os.getenv("WS_PORT", 12345)),
        log_level=str(os.getenv("LOGLEVEL", "info")).lower(),
        ws="websockets",
    )
