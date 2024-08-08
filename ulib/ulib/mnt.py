import logging
import pathlib
from typing import Optional

import libmount  # python3-libmount

from . import exc


class UlibMntError(exc.UlibError):
    ...


def mount_guest(src: pathlib.Path, off: int, mnt: pathlib.Path):
    """Mount guest disk.
    # mount -o loop,ro,offset=$2 $IMAGES/$1 $MNTDIR
    :exceptions:
    - ...
    """
    mount(src, mnt, f"loop,ro,offset={off}")


def mount(src: pathlib.Path, mnt: pathlib.Path, opts: Optional[str] = None):
    """Mount real device."""
    logging.debug("Mount %s => %s with %s", str(src), str(mnt), opts)
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
    """Umount device."""
    ctx = libmount.Context()
    ctx.target = str(mnt)
    ctx.umount()
