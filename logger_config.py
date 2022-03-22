import datetime
import logging
import sys

import structlog
from structlog import wrap_logger
from structlog.processors import JSONRenderer
from structlog.stdlib import filter_by_level

logging.basicConfig(stream=sys.stdout, format="%(message)s", level=logging.DEBUG)


def add_timestamp(_, __, event_dict):
    event_dict["timestamp"] = datetime.datetime.utcnow()
    return event_dict


def censor_secrets(_, __, event_dict: dict):
    pw = event_dict.get("password")
    api_key = event_dict.get("api_key")
    if pw:
        event_dict["password"] = "*CENSORED*"

    if api_key:
        event_dict["api_key"] = api_key[:2] + "******" + api_key[-2:]  # getting first and last 2 chars of API key
    return event_dict


log = wrap_logger(
    logging.getLogger(__name__),
    processors=[
        structlog.processors.add_log_level,
        add_timestamp,
        filter_by_level,
        censor_secrets,
        JSONRenderer(indent=1, sort_keys=True)
    ]
)
