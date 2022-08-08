"""Subprocess wrapper"""
from typing import Type
import logging
import subprocess
# 3. local
from . import exc


def sp(cmds: list[str], cls: Type[exc.UlibTextError]):
    """
    Exec given command with options.
    :param cmds: command and its options
    :param cls: exception class
    """
    logging.debug(' '.join(cmds))
    cp: subprocess.CompletedProcess = subprocess.run(
        cmds,
        capture_output=True,
        encoding='utf-8'
    )
    if cp.returncode != 0:
        msg = f"{cmds[0]} error ({cp.returncode}): {cp.stderr}"
        logging.error(msg)
        raise cls(msg)
