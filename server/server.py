import os
import json
from typing import Dict
import random
import asyncio

import uvicorn
from fastapi import FastAPI, WebSocket
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


@app.get("/")
def http_endpoint():
    return producer()


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host=os.getenv("WS_HOST", "0.0.0.0"),
        port=os.getenv("WS_PORT", 12345),
        log_level=os.getenv("LOGLEVEL", "info"),
        ws="websockets",
    )
