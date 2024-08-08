"""Rsync wrapper"""
import pathlib
import subprocess
from typing import Optional, Iterable

import sysrsync  # Fx ok, ~~EL9~~ - handmade

# 3. local
from . import exc


class UlibRsyncError(exc.UlibError):
    ...


def rsync_raw(cmds: list[str]):
    """
    run the built rsync command as a subprocess
    :return: True if ok
    :todo: shutil.which('rsync')
    """
    cp: subprocess.CompletedProcess = subprocess.run(
        ['rsync'] + cmds,
        capture_output=True,
        encoding='utf-8'
    )
    if cp.returncode != 0:
        msg = f"Rsync error ({cp.returncode}): {cp.stderr}"
        raise UlibRsyncError(msg)


def rsync(src: pathlib.Path, dst: pathlib.Path, opts: Optional[Iterable[str]] = None):
    sysrsync.run(source=str(src), destination=str(dst), syn_source_content=True, options=opts)
