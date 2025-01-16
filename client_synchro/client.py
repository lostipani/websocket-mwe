import json
from typing import List
from websockets.sync.client import connect

from commons.logger import logger
from commons.parser import get_URI


def main(data: List[int]) -> None:
    try:
        with connect(get_URI()) as websocket:
            for message in websocket:
                data.append(json.loads(message)["value"])
                logger.info(data)
    except ConnectionRefusedError as error:
        logger.error(error)
        raise


if __name__ == "__main__":
    data: List[int] = []
    main(data)
