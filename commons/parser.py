import os
from typing import Any, Dict
from .logger import logging


def get_URI():
    try:
        return f"ws://{os.environ['WS_HOST']}:{os.environ['WS_PORT']}/ws"
    except KeyError:
        logging.error("missing WS_HOST and/or WS_PORT as env vars")
        raise


def get_server_period() -> float:
    try:
        return float(os.environ["SERVER_PERIOD"])
    except KeyError:
        logging.error("missing server production period, in seconds")
        raise


def get_listener_period() -> float:
    try:
        return float(os.environ["LISTENER_PERIOD"])
    except KeyError:
        logging.error("missing client's listener frequency, in seconds")
        raise


def get_consumer_period() -> float:
    try:
        return float(os.environ["CONSUMER_PERIOD"])
    except KeyError:
        logging.error("missing client's consumer frequency, in seconds")
        raise


def get_broker_params() -> Dict[str, Any]:
    try:
        return {"host": (os.environ["BROKER_HOST"])}
    except KeyError:
        logging.error("missing broker's hostname")
        raise
