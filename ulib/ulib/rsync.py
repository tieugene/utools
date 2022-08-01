"""Rsync wrapper"""
# 1. std
import logging
import subprocess
# 3. local
from . import exc


class UlibRsyncError(exc.UlibTextError):
    """Config loading exceptions."""
    name = "Rsync"


def rsync(cmds: list[str]):
    """
    run the built rsync command as a subprocess
    :return: True if ok
    :todo: shutil.which('rsync')
    """
    logging.debug("rsync %s" % ' '.join(cmds))
    cp: subprocess.CompletedProcess = subprocess.run(
        ['rsync'] + cmds,
        capture_output=True,
        encoding='utf-8'
    )
    if cp.returncode != 0:
        msg = f"Rsync error ({cp.returncode}): {cp.stderr}"
        logging.error(msg)
        raise UlibRsyncError(msg)
