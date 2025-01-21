import json
import asyncio
from typing import List, Tuple
from websockets.asyncio.client import connect

from commons.logger import logger
from commons.parser import get_URI, get_listener_period
from commons.broker import Bus

async def listener(URI: str, bus: Bus, period: float) -> None:
    try:
        async with connect(URI) as websocket:
            async for message in websocket:
                bus.add(json.loads(message)["value"])
                await asyncio.sleep(period)
    except ConnectionRefusedError as error:
        logger.error(error)
        raise


async def main(bus: Bus):
    tasks = [
        asyncio.create_task(listener(get_URI(), bus, get_listener_period())),
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    bus = Bus.factory(data=[0])
    asyncio.run(main(bus))
