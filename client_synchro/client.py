import json
from websockets.sync.client import connect

from commons.logger import logger
from commons.parser import get_URI
from commons.broker import Broker


def main(broker: Broker) -> None:
    try:
        with connect(get_URI()) as websocket:
            for message in websocket:
                broker.add(json.loads(message)["value"])
                logger.info(broker)
    except ConnectionRefusedError as error:
        logger.error(error)
        raise


if __name__ == "__main__":
    broker = Broker.factory(backend=[0])
    main(broker)
