import os
from .logger import logging


def get_URI():
    try:
        return f"ws://{os.environ['WS_HOST']}:{os.environ['WS_PORT']}/ws"
    except KeyError:
        logging.error("missing WS_HOST and/or WS_PORT as env vars")
        raise


def get_server_frequency() -> float:
    try:
        return float(os.environ["SERVER_FREQUENCY"])
    except KeyError:
        logging.error("missing server production frequency, in seconds")
        raise
