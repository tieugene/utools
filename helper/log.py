"""Logging subsystem.
Console out obly (for systemd).
"""

import sys
import logging
import logging.handlers

LOG_LEVEL = (
    logging.NOTSET,
    logging.CRITICAL,
    logging.ERROR,
    logging.WARNING,
    logging.INFO,
    logging.DEBUG
)


def setLogger(lvl: int):
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    logger.setLevel(LOG_LEVEL[lvl])


''' Фокус не удался
handlers.SMTPHandler(
    mailhost=(cfg['smtp'], 465),
    fromaddr=cfg['mailfrom'],
    toaddrs=[cfg['mailto']],
    subject="Subject",
    credentials=(cfg['mailfrom'], cfg['mailpass'])
))
'''
