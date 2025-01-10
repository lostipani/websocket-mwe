import os
import json
import logging
import numpy as np
import threading
import asyncio
from typing import List
from websockets.sync.client import connect

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


def calculator(data: List[int]) -> None:
    arr = np.array(data)
    logging.info("mean: %.6f and std: %.6f", np.mean(arr), np.std(arr))


def main(data: List[int]):
    try:
        URI = f"ws://{os.environ["WS_HOST"]}:{os.environ["WS_PORT"]}/ws"
    except KeyError:
        logging.error("missing WS_HOST and/or WS_PORT as env vars")
        raise

    threads = [
        asyncio.to_thread(receiver, URI, data),
        threading.Thread(target=calculator, args=(data,)),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    data: List[int] = []
    main(data)
