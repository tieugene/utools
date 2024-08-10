"""Main file"""
# 1. std
import pathlib
import shutil
from typing import List, Optional
# 2. 3rd
import sh
# 3. local
from . import exc, rsync, mnt, pack


class UlibBackupError(exc.UlibError):
    ...


# TODO: class MyPath(patlib.Path)
# TODO: with path == os.getcwd()+os.chdir()...+os.chdir
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
def dump_self(dst_f: pathlib.Path):
    # dump -0 -z -f $BACKUPDIR/$DAILY/$TODAY/vms_root.gz / > /dev/null
    sh.dump('-0', '-z', '-f', str(dst_f.with_suffix('gz')), '/')


def dir_rotate(path: pathlib.Path, count: int):
    """Rotate subfolders."""
    for d in sorted(list(path.iterdir()))[:-count]:
        dir_rm(d, recur=True)


def __cpal(src_d: pathlib.Path, dst_d: pathlib.Path, subj: str):
    sh.cp('-al', str(src_d / subj), str(dst_d / subj))


def xly(src: pathlib.Path, dst: pathlib.Path, ymd: str, count: int):
    """Handle weekly/monthly"""
    __cpal(src, dst, ymd)
    dir_rotate(dst, count)


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
    :todo: rm xtra attrs (owner, rights etc: -a==)
    """
    opts = ['-axAXH', '--modify-window=1', '--del']
    if prev:
        opts.append(f"--link-dest=../../{prev}/{subj}")
    rsync.rsync(src / subj, dst / subj, opts)


def backup_1c7(src: pathlib.Path, dst: pathlib.Path):
    """
    :param src: Source folder with 1c7 folders
    :param dst: Destination folder
    """
    for d in src.iterdir():
        if not d.is_dir():
            continue
        pack.pack_dir(d, dst, ('*.md', '*.dd', '*.dbf'))


def backup_1c8(src: pathlib.Path, dst: pathlib.Path):
    for d in src.iterdir():
        if not d.is_dir():
            continue
        files = list(d.glob('1Cv8.1CD', case_sensitive=False))
        if not files:
            continue
        file = files[0]
        pack.pack_file(file, dst / (d.name + '.' + file.name))


def backup_vdrive(src_f: pathlib.Path, dst_d: pathlib.Path):
    """Backup vdrive image into folder."""
    pack.pack_file(src_f, dst_d / src_f.name)
