import json
from typing import List
from websockets.sync.client import connect

from commons.logger import logger
from commons.parser import get_URI
from commons.broker import Bus


def main(bus: Bus) -> None:
    try:
        with connect(get_URI()) as websocket:
            for message in websocket:
                bus.add(json.loads(message)["value"])
                logger.info(bus)
    except ConnectionRefusedError as error:
        logger.error(error)
        raise


if __name__ == "__main__":
    bus = Bus.factory(data=[0])
    main(bus)
