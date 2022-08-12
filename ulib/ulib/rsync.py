"""Rsync wrapper"""
# 1. std
import logging
import subprocess
# 3. local
from . import exc, sp


class UlibRsyncError(exc.UlibTextError):
    """Config loading exceptions."""
    name = "Rsync"


def rsync(opts: list[str]):
    """
    Run the built rsync command as a subprocess.
    :param opts: rsync CLI options
    :todo: shutil.which('rsync')
    """
    sp.sp(['rsync'] + opts, UlibRsyncError)
