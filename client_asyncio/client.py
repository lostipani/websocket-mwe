import json
import numpy as np
import asyncio
from typing import List, Tuple
from websockets.asyncio.client import connect

from commons.logger import logger
from commons.parser import get_URI


async def receiver(URI: str, data: List[int]) -> None:
    try:
        async with connect(URI) as websocket:
            async for message in websocket:
                data.append(json.loads(message)["value"])
                await asyncio.sleep(0)
    except ConnectionRefusedError as error:
        logger.error(error)
        raise


async def calculator(data: List[int]) -> Tuple[float, float]:
    while True:
        arr = np.array(data)
        if arr.size > 0:
            logger.debug(data)
            logger.info("mean: %.6f and std: %.6f", np.mean(arr), np.std(arr))
        else:
            logger.warning("no data")
        await asyncio.sleep(1)


async def main(data: List[int]):
    tasks = [
        asyncio.create_task(receiver(get_URI(), data)),
        asyncio.create_task(calculator(data)),
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    data: List[int] = []
    asyncio.run(main(data))
