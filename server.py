import asyncio
import random
import websockets
import json


async def handler(websocket):
    while True:
        data = {"value": random.randint(-1000, 1000)}
        try:
            await websocket.send(json.dumps(data))
        except websockets.ConnectionClosedOK:
            break
        await asyncio.sleep(1)


async def main():
    async with websockets.serve(handler, "localhost", 12345) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
