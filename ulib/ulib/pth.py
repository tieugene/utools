"""Path helpers."""
import pathlib
import shutil
from typing import List
from . import exc

# TODO: class MyPath(patlib.Path)
# TODO: with path == os.getcwd()+os.chdir()...+os.chdir


class UlibPathError(exc.UlibError):
    ...


def dir_exists(path: pathlib.Path) -> bool:
    try:
        return path.exists()
    except PermissionError as e:
        raise UlibPathError(str(e)) from e


def dir_empty(path: pathlib.Path) -> bool:
    """Chrck folder is empty.
    :exceptions:
    - [ ] not exists
    - [ ] not folder
    - [ ] access denied
    """
    return not bool(dir_list(path))


def dir_mounted(path: pathlib.Path) -> bool:
    """Check folder is mount.
    :exceptions:
    - [ ] not exists
    - [ ] not folder
    - [ ] access denied
    """
    return path.is_mount()


def dir_rm(path: pathlib.Path, recur: bool = False):
    """Remove folder.
    :exceptions:
    - [ ] not exists
    - [ ] not folder
    - [ ] not empty (?)
    - [ ] access denied
    """
    if recur:
        shutil.rmtree(str(path))
    else:
        path.rmdir()


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
        raise UlibPathError(str(e)) from e
    except NotADirectoryError as e:
        raise UlibPathError(str(e)) from e
    except PermissionError as e:
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
    except FileNotFoundError as e:
        raise UlibPathError(str(e)) from e
    except NotADirectoryError as e:
        raise UlibPathError(str(e)) from e
    except FileExistsError as e:
        raise UlibPathError(str(e)) from e
    except PermissionError as e:
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
