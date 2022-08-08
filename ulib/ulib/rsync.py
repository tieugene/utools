"""Rsync wrapper"""
# 1. std
import logging
import subprocess
# 3. local
from . import exc


class UlibRsyncError(exc.UlibTextError):
    """Config loading exceptions."""
    name = "Rsync"


def rsync(opts: list[str]):
    """
    Run the built rsync command as a subprocess.
    :param opts: rsync CLI options
    :return: True if ok
    :todo: shutil.which('rsync')
    """
    cmds = ['rsync'] + opts
    logging.debug(' '.join(cmds))
    cp: subprocess.CompletedProcess = subprocess.run(
        cmds,
        capture_output=True,
        encoding='utf-8'
    )
    if cp.returncode != 0:
        msg = f"Rsync error ({cp.returncode}): {cp.stderr}"
        logging.error(msg)
        raise UlibRsyncError(msg)
