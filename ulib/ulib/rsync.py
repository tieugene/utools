"""Rsync wrapper"""
import logging
import pathlib
import subprocess
from typing import Optional, Iterable

import sysrsync  # Fx ok, ~~EL9~~ - handmade
import sysrsync.exceptions

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


def rsync(src: pathlib.Path, dst: pathlib.Path, opts: Iterable[str]):
    """:exceptions:
    - [x] src not exists (RsyncError)
    - [ ] src is not folder (no effect if dst exists)
    - [x] src access denied (RsyncError)
    - [x] dst parent not exists (RsyncError)
    - [x] dst parent is not folder (RsyncError)
    - [x] dst [parent] access denied (RsyncError)
    - [x] dst is file (RsyncError)
    """
    logging.debug("Rsync %s => %s", src, dst)
    try:
        sysrsync.run(source=str(src), destination=str(dst), options=opts)
    except sysrsync.exceptions.RsyncError as e:
        raise UlibRsyncError(str(e)) from e
