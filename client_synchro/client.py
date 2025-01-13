import json
import numpy as np
from typing import List
from websockets.sync.client import connect

from commons.logger import logging
from commons.parser import parse_URI


def main(data: List[int]) -> None:
    try:
        with connect(parse_URI()) as websocket:
            for message in websocket:
                data.append(json.loads(message)["value"])
                arr = np.array(data)
                logging.info(f"mean: {np.mean(arr)} and std: {np.std(arr)}")
    except ConnectionRefusedError as error:
        logging.error(error)
        raise


if __name__ == "__main__":
    data: List[int] = []
    main(data)
