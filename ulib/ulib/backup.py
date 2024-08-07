#!/usr/bin/env python3
"""Main file"""
# 1. std
import pathlib
from typing import List, Optional
# 2. 3rd
import sh
# local
from . import exc


class UlibBackupError(exc.UlibError):
    """Basic error"""
    msg: str

    def __init__(self, msg: str):
        super().__init__(self)
        self.msg = msg


def dir_list(path: pathlib.Path) -> List[str]:
    """
    :exceptions:
    - not exists
    - not folder
    - access denied
    """
    return sorted([x.name for x in path.iterdir()])


def dir_mk(path: pathlib.Path):
    """Create dir (if not exists).
    :exceptions:
    - parent not exists
    - paren is not dir
    - access denied
    - exists and is not dir
    """
    ...


def dir_rotate(path: pathlib.Path, count: int):
    """Rotate subfolders.
    :exceptions:
    - is not dir
    - access denied
    """
    ...


def guest_mount(src: pathlib.Path, dst: pathlib.Path):
    """Mount guest disk.
    :exceptions:
    - ...
    """
    ...


def guest_umount(mnt: pathlib.Path):
    """Umount guest disk"""
    ...


def mount(src: pathlib.Path, mnt: pathlib.Path):
    """Mount real device."""


def umount(mnt: pathlib.Path):
    """Umount device."""


def rsync_local(dev: str, mnt: str, src: pathlib.Path):
    ...
    # mount dest
    # rsync
    # umount


def cpal():
    # cp -al | mk hardlink
    ...


def backup_dir(src: pathlib.Path, dst: pathlib.Path, subj: str, prev: Optional[str] = None):
    """Backup a folder.
    :exceptions:
    - src not exists
    - src is not folder
    - dst not exists
    - dst is not folder
    - subj not exists
    """
    # rsync -axAXH $addon --modify-window=1 --del --link-dest=
    ...


def __backup_1c(src: pathlib.Path, dst: pathlib.Path, opts: str):
    """Backup 1C folders."""
    # for each subfolder:
    # 7za
    ...


def backup_1c7(src: pathlib.Path, dst: pathlib.Path):
    __backup_1c(src, dst, "1[Cc][Vv]7.?[Dd] *.[Dd][Bb][Ff]")


def backup_1c8(src: pathlib.Path, dst: pathlib.Path):
    __backup_1c(src, dst, "*")


def weekly(src: pathlib.Path, dst: pathlib.Path, ymd: str, count: int):
    ...
    # # vhost.poweroff (нельзя; iptables)
    # # 7za vdisks
    # # dump self
    # # poweron
    # cpal|hardlink daily
    # dir_rotate


def monthly(count: int):
    ...
    # cpal|hlink weekly
    # dir_rotate(count)
