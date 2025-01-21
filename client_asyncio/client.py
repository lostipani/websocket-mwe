import json
import asyncio
from typing import Tuple
from websockets.asyncio.client import connect

from commons.logger import logger
from commons.parser import get_URI, get_listener_period, get_consumer_period
from commons.broker import Broker


async def listener(URI: str, broker: Broker, period: float) -> None:
    try:
        async with connect(URI) as websocket:
            async for message in websocket:
                broker.add(json.loads(message)["value"])
                await asyncio.sleep(period)
    except ConnectionRefusedError as error:
        logger.error(error)
        raise


async def consumer(broker: Broker, period: float) -> Tuple[float, float]:
    while True:
        if broker.size() > 0:
            logger.info(broker)
        else:
            logger.warning("no data")
        await asyncio.sleep(period)


async def main(broker: Broker):
    tasks = [
        asyncio.create_task(
                listener(get_URI(), broker, get_listener_period())
            ),
        asyncio.create_task(consumer(broker, get_consumer_period())),
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    broker = Broker.factory(backend=[0])
    asyncio.run(main(broker))
