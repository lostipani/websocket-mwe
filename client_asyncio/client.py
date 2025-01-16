import json
import asyncio
from typing import List, Tuple
from websockets.asyncio.client import connect

from commons.logger import logger
from commons.parser import get_URI, get_listener_period, get_consumer_period


async def listener(URI: str, data: List[int], period: float) -> None:
    try:
        async with connect(URI) as websocket:
            async for message in websocket:
                data.append(json.loads(message)["value"])
                await asyncio.sleep(period)
    except ConnectionRefusedError as error:
        logger.error(error)
        raise


async def consumer(data: List[int], period: float) -> Tuple[float, float]:
    while True:
        if len(data) > 0:
            logger.info(data)
        else:
            logger.warning("no data")
        await asyncio.sleep(period)


async def main(data: List[int]):
    tasks = [
        asyncio.create_task(listener(get_URI(), data, get_listener_period())),
        asyncio.create_task(consumer(data, get_consumer_period())),
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    data: List[int] = []
    asyncio.run(main(data))
