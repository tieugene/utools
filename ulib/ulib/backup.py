"""Main file"""
# 1. std
import pathlib
from typing import List, Optional
# 2. 3rd
import sh
# local
from . import exc, rsync, mnt


class UlibBackupError(exc.UlibError):
    ...


def dir_exists(path: pathlib.Path) -> bool:
    try:
        return path.exists()
    except PermissionError as e:
        raise UlibBackupError(str(e)) from e


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


def dir_rm(path: pathlib.Path):
    """Remove folder.
    :exceptions:
    - [ ] not exists
    - [ ] not folder
    - [ ] not empty (?)
    - [ ] access denied
    """
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
        raise UlibBackupError(str(e)) from e
    except NotADirectoryError as e:
        raise UlibBackupError(str(e)) from e
    except PermissionError as e:
        raise UlibBackupError(str(e)) from e


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
        raise UlibBackupError(str(e)) from e
    except NotADirectoryError as e:
        raise UlibBackupError(str(e)) from e
    except FileExistsError as e:
        raise UlibBackupError(str(e)) from e
    except PermissionError as e:
        raise UlibBackupError(str(e)) from e


# ----
def dir_rotate(path: pathlib.Path, count: int):
    """Rotate subfolders.
    :exceptions:
    - is not dir
    - access denied
    """
    # sh.rmdir -r
    ...


def cpal():
    # sh.cp -al
    ...


def xly(src: pathlib.Path, dst: pathlib.Path, ymd: str, count: int):
    """Handle weekly/monthly"""
    ...
    # cpal src / ymd => dst / ymd
    # dir_rotate(dst, count)


def rsync_local(dev: pathlib.Path, dst: pathlib.Path, src: pathlib.Path):
    mnt.mount(dev, dst)
    rsync.rsync(src, dst / src.name, ['-azAXH', '--del'])
    mnt.umount(dst)


def backup_dir(src: pathlib.Path, dst: pathlib.Path, subj: str, prev: Optional[str] = None):
    """Backup an NTFS folder.
    :param: src: windows vdisk root
    :param: dst: daily root
    :param: subj: folder to sync
    :param: prev: folder to --link-dest
    :note: --link-dest is _exactly_ '../../{prev}/{subj}'
    :exceptions:
    - [ ] src not exists
    - [ ] dst not exists
    - [ ] src/subj not exists
    """
    opts = ['-axAXH', '-modify-window=1', '--del']
    if prev:
        opts.append(f"--link-dest=../../{prev}/subj")
    rsync.rsync(src / subj, dst / subj, opts)


def __backup_1c(src: pathlib.Path, dst: pathlib.Path, opts: str):
    """Backup 1C folders."""
    #
    # for each subfolder:
    #   7za
    ...


def backup_1c7(src: pathlib.Path, dst: pathlib.Path):
    __backup_1c(src, dst, "1[Cc][Vv]7.?[Dd] *.[Dd][Bb][Ff]")


def backup_1c8(src: pathlib.Path, dst: pathlib.Path):
    __backup_1c(src, dst, "*")  # FIXME: 1Cv8.1CD
