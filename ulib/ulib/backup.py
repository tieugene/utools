"""Main file"""
# 1. std
import pathlib
from typing import List, Optional
# 2. 3rd
import sh
# local
from . import exc


class UlibBackupError(exc.UlibError):
    ...


def dir_exists(path: pathlib.Path) -> bool:
    try:
        return path.exists()
    except PermissionError as e:
        raise UlibBackupError(str(e)) from e


def dir_list(path: pathlib.Path) -> List[str]:
    """
    :exceptions:
    - [x] not exists
    - [x] not folder
    - [x] access denied
    """
    try:
        return sorted([x.name for x in path.iterdir()])
    except FileNotFoundError as e:
        raise UlibBackupError(str(e)) from e
    except NotADirectoryError as e:
        raise UlibBackupError(str(e)) from e
    except PermissionError as e:
        raise UlibBackupError(str(e)) from e


def dir_mk(path: pathlib.Path):
    """Create dir [if not exists].
    :exceptions:
    - [ ] parent not exists
    - [ ] paren is not dir
    - [x] access denied
    - [x] exists
    - [ ] exists and is not dir
    :todo: if not exists
    """
    try:
        path.mkdir()
    except FileExistsError as e:
        raise UlibBackupError(str(e)) from e
    except PermissionError as e:
        raise UlibBackupError(str(e)) from e


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


def xly(src: pathlib.Path, dst: pathlib.Path, ymd: str, count: int):
    ...
    # cpal|hardlink daily
    # dir_rotate
