import os
import json
import logging
import numpy as np
from typing import List
from websockets.sync.client import connect

logging.basicConfig(
    format="%(message)s",
    level=os.getenv("LOGLEVEL", "INFO"),
)


def main(data: List[int]) -> None:
    try:
        URI = f"ws://{os.environ["WS_HOST"]}:{os.environ["WS_PORT"]}/ws"
    except KeyError as error:
        logging.error("missing WS_HOST and/or WS_PORT as env vars")
        raise

    try:
        with connect(URI) as websocket:
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
