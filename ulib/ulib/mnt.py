"""Mount things.
TODO:
- with mount:
"""
import logging
import pathlib
from typing import Optional

import libmount  # python3-libmount

from . import exc


class UlibMntError(exc.UlibError):
    ...


def mount_guest(src: pathlib.Path, off: int, mnt: pathlib.Path):
    """Mount NTFS guest disk.
    :exceptions:
    - ...
    """
    mount(src, mnt, f"loop,ro,fmask=111,offset={off}")


def mount(src: pathlib.Path, mnt: pathlib.Path, opts: Optional[str] = None):
    """Mount real device.
    :exceptions:
    - ...
    """
    logging.debug("Mount %s => %s with %s", src, mnt, opts)
    try:
        ctx = libmount.Context()
        ctx.source = str(src)
        ctx.target = str(mnt)
        if opts:
            ctx.options = opts
        ctx.mount()
    except libmount.Error as e:
        raise UlibMntError(str(e)) from e


def umount(mnt: pathlib.Path):
    """Umount device.
    :exceptions:
    - ...
    """
    if mnt.is_mount():
        logging.debug("Umount %s", mnt)
        ctx = libmount.Context()
        ctx.target = str(mnt)
        ctx.umount()
