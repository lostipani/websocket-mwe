import json
import asyncio
from websockets.asyncio.client import connect

from commons.logger import logger
from commons.parser import get_URI, get_listener_period, get_broker_params
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


async def main(broker: Broker):
    tasks = [
        asyncio.create_task(listener(get_URI(), broker, get_listener_period()))
    ]
    asyncio.gather(*tasks)


if __name__ == "__main__":
    broker_params = get_broker_params()
    broker = Broker.factory(
        backend="rabbitmq",
        queue="test",
        host=broker_params.get("host"),
        routing_key="test",
    )
    asyncio.run(main(broker))
