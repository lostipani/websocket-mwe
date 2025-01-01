import os
import json
import asyncio
import logging
import numpy as np
from typing import List, Any
from websockets.asyncio.client import connect

logging.basicConfig(
    format="%(message)s",
    level=os.getenv("LOGLEVEL", "INFO"),
)


async def main(data: List[Any]):
    try:
        URI = f"ws://{os.environ["WS_HOST"]}:{os.environ["WS_PORT"]}/ws"
    except KeyError as error:
        logging.error("missing WS_HOST and/or WS_PORT as env vars")
        raise

    try:
        async with connect(URI) as websocket:
            async for message in websocket:
                data.append(json.loads(message)["value"])
                arr = np.array(data)
                logging.info(f"mean: {np.mean(arr)} and std: {np.std(arr)}")
    except ConnectionRefusedError as error:
        logging.error(error)
        raise


if __name__ == "__main__":
    data = list()
    asyncio.run(main(data))
