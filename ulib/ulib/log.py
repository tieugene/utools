"""Logging subsystem.
Console out obly (for systemd).
"""
import io
import logging
from typing import Optional

LOG_LEVEL = (
    logging.NOTSET,
    logging.CRITICAL,
    logging.ERROR,
    logging.WARNING,
    logging.INFO,
    logging.DEBUG
)


def set_logger(lvl: int, with_str: bool = False) -> Optional[io.StringIO]:
    logging.basicConfig(level=lvl)
    if with_str:
        log_capture_string = io.StringIO()
        ch = logging.StreamHandler(log_capture_string)
        ch.setLevel(lvl)
        logging.getLogger().addHandler(ch)
        return log_capture_string
