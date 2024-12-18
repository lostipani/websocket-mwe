import os
import json
import random
import logging
import asyncio
import websockets

logging.basicConfig(
    format="%(message)s",
    level=os.getenv("LOGLEVEL", "INFO"),
)


async def handler(websocket):
    while True:
        data = {"value": random.gauss(0, 1)}
        try:
            await websocket.send(json.dumps(data))
        except websockets.ConnectionClosedOK:
            break
        await asyncio.sleep(1)


async def main():
    async with websockets.serve(
        handler,
        os.getenv("WSHOST", "0.0.0.0"),
        os.getenv("WSPORT", 12345),
        logger=logging.getLogger("websockets.server"),
    ) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
