"""Path helpers."""
import os
import pathlib
import shutil
from typing import List
from . import exc

# TODO: class MyPath(patlib.Path)
# TODO: with path == os.getcwd()+os.chdir()...+os.chdir


class UlibPathError(exc.UlibError):
    ...


def exists(path: pathlib.Path) -> bool:
    try:
        return path.exists()
    except PermissionError as e:
        raise UlibPathError(str(e)) from e


def dir_empty(path: pathlib.Path) -> bool:
    """Check folder is empty.
    :exceptions:
    - [x] not exists
    - [x] not folder
    - [x] access denied
    """
    return not bool(dir_list(path))


def dir_mounted(path: pathlib.Path) -> bool:
    """Check folder is mount.
    :note: no exceptions"""
    return path.is_mount()


def dir_rm(path: pathlib.Path, recur: bool = False):
    """Remove folder.
    :exceptions:
    - [x] not exists
    - [x] not folder
    - [x] not empty (OSError)
    - [x] access denied
    """
    try:
        if recur:
            shutil.rmtree(str(path))
        else:
            path.rmdir()
    except (FileNotFoundError, NotADirectoryError, PermissionError, OSError) as e:
        raise UlibPathError(str(e)) from e


def dir_list(path: pathlib.Path) -> List[str]:
    """
    :exceptions:
    - [x] not exists
    - [x] not folder
    - [x] access denied
    """
    try:
        return sorted([x.name for x in path.iterdir()])
    except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
        raise UlibPathError(str(e)) from e


def dir_mk(path: pathlib.Path):
    """Create dir [if not exists].
    :exceptions:
    - [x] parent not exists (FileNotFoundError)
    - [x] paren is not dir (NotADirectoryError)
    - [x] access denied (PermissionError)
    - [x] exists (FileExistsError)
    - exists and is not dir
    :todo: if not exists
    """
    try:
        path.mkdir()
    except (FileNotFoundError, NotADirectoryError, PermissionError, FileExistsError) as e:
        raise UlibPathError(str(e)) from e


def dir_rotate(path: pathlib.Path, count: int):
    """Rotate subfolders.
    :exceptions:
    - not exists
    - not dir
    - access denied
    """
    for d in sorted(list(path.iterdir()))[:-count]:
        dir_rm(d, recur=True)


def cpal(src_d: pathlib.Path, dst_d: pathlib.Path):
    """cp -al.
    :exceptions:
    - [x] src not exists (FileNotFoundError)
    - [x] dst is not dir
    - [x] src/dst access denied (PermissionError)
    - [x] dst exists (FileExistsError)
    """
    try:
        # sh.cp('-al', str(src_d), str(dst_d / src_d.name))
        shutil.copytree(str(src_d), str(dst_d / src_d.name), copy_function=os.link)
    except (FileNotFoundError, FileExistsError, NotADirectoryError, PermissionError) as e:
        raise UlibPathError(str(e)) from e
