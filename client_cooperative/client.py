import os
import json
import logging
import numpy as np
import asyncio
from typing import List, Tuple
from websockets.asyncio.client import connect

logging.basicConfig(
    format="%(message)s",
    level=os.getenv("LOGLEVEL", "INFO"),
)


async def receiver(URI: str, data: List[int]) -> None:
    try:
        async with connect(URI) as websocket:
            async for message in websocket:
                data.append(json.loads(message)["value"])
                await asyncio.sleep(0)
    except ConnectionRefusedError as error:
        logging.error(error)
        raise


async def calculator(data: List[int]) -> Tuple[float, float]:
    while True:
        arr = np.array(data)
        if arr.size > 0:
            logging.info("mean: %.6f and std: %.6f", np.mean(arr), np.std(arr))
        else:
            logging.warning("no data")
        await asyncio.sleep(1)


async def main(data: List[int]):
    try:
        URI = f"ws://{os.environ["WS_HOST"]}:{os.environ["WS_PORT"]}/ws"
    except KeyError:
        logging.error("missing WS_HOST and/or WS_PORT as env vars")
        raise

    tasks = [
        asyncio.create_task(receiver(URI, data)),
        asyncio.create_task(calculator(data)),
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    data: List[int] = []
    asyncio.run(main(data))
