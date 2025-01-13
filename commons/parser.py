import os
from .logger import logging


def parse_URI():
    try:
        return f"ws://{os.environ['WS_HOST']}:{os.environ['WS_PORT']}/ws"
    except KeyError:
        logging.error("missing WS_HOST and/or WS_PORT as env vars")
        raise
