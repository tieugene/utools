"""Main file"""
# 1. std
import pathlib
from typing import Optional
# 2. 3rd
import sh
# 3. local
from . import exc, rsync, mnt, pack, pth


class UlibBackupError(exc.UlibError):
    ...


def __cpal(src_d: pathlib.Path, dst_d: pathlib.Path, subj: str):
    # shutil.copytree(src, dst, copy_function=os.link)
    sh.cp('-al', str(src_d / subj), str(dst_d / subj))


def xly(src: pathlib.Path, dst: pathlib.Path, ymd: str, count: int):
    """Handle weekly/monthly"""
    __cpal(src, dst, ymd)
    pth.dir_rotate(dst, count)


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


def dump_self(dst_f: pathlib.Path):
    # dump -0 -z -f $BACKUPDIR/$DAILY/$TODAY/vms_root.gz / > /dev/null
    sh.dump('-0', '-z', '-f', str(dst_f.with_suffix('gz')), '/')


def rsync_local(dev: pathlib.Path, dst: pathlib.Path, src: pathlib.Path):
    mnt.mount(dev, dst)
    rsync.rsync(src, dst / src.name, ['-azAXH', '--del'])
    mnt.umount(dst)
