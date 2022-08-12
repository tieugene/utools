#!/usr/bin/env python3
"""Backup
:todo: mail report queue
:todo: --dry-run
"""
# 1. std
import os
import datetime
import logging
import shutil
from pathlib import Path
# 32. rds
# python-libvirt (F34, RH8, ~CO7~)
# python-lxc (F34, RH8, ~CO7~)
import libvirt
# 3. local
from ulib import exc, pre, log, sp, rsync, virt, vdrive
# x. const (TODO: to cfg | default)
DIR_D = 'daily'
DIR_W = 'weekly'
DIR_M = 'monthly'
OPTS_7Z = ['-t7z', '-m0=lzma', '-mx=9', '-mfb=64', '-md=32m', '-ms=on']


class UlibBackupError(exc.UlibTextError):
    name = "Backup"


def __rsync(spath: Path, dpath: Path, by: Path = None) -> bool:
    """Rsync spath as dppath using by as link-dest
    :param spath: Abs source path to backup
    :param dpath: Abs dest path ('/…/YYMMDD')
    :param by: Abs prev path ('yesterday', '/…/YYMMDD')
    :return: True on success
    """
    if not spath.is_dir():
        logging.error(f"__rsync: Source dir '{spath}' not found")
        return False
    __tail = spath.name
    __dest = dpath / __tail
    if __dest.exists():
        logging.error(f"Dest '{__dest}' already exists")
        return False
    opts = ['-axAXH', '--modify-window=1', '--del']
    __prev = by / __tail
    if not __prev.is_dir():
        logging.info(f"Prev dir '{__prev}' not found")
    else:
        opts.append(f"--link-dest={os.path.relpath(__prev, __dest)}")
    opts.extend([str(spath) + '/', str(__dest)])
    dpath.mkdir(exist_ok=True)
    # print(' '.join(cmds))
    rsync.rsync(opts)
    return True


def __7za(spath: Path, dpath: Path, mask: str = '*') -> bool:
    """Pack subfolders of given spath into dpath
    :param spath: Abs source path to backup
    :param dpath: Abs dest path ('/…/YYMMDD')
    :param mask: What to pack
    :return: True on success
    :todo: partial success
    """
    if not spath.is_dir():
        logging.error(f"7za: Source dir '{spath}' not found")
        return False
    for d in spath.iterdir():
        if not d.is_dir():
            logging.warning(f"Not a dir: '{d}'")
            continue
        cwd = Path.cwd()
        os.chdir(d)
        opts = ['7za', 'a'] + OPTS_7Z + [str(dpath / d.name) + '.7za', mask]
        # print(opts)
        dpath.mkdir(exist_ok=True)
        sp.sp(opts, UlibBackupError)
        os.chdir(cwd)
    return True


def cpal(spath: Path, dpath: Path):
    """'cp -al src => dst"""
    sp.sp(['cp', '-al', spath, dpath], UlibBackupError)


def rotate_dir(path: Path, size: int) -> bool:
    """Rotates folder content by given items"""
    if not path.is_dir():
        logging.error(f"Rotate: rotating dir '{path}' not found")
        return False
    for d in sorted(path.iterdir())[:-size]:
        if not d.is_dir():
            logging.warning(f"Rotate: '{d}' is not dir")
            continue
        print(f"Rmtree '{d}'")
        # shutil.rmtree(d)


def daily(data: dict) -> bool:
    """Daily tasks.
    :todo: lxc guest
    :todo: force backup flag
    :todo: umount anyway
    """
    mnt2: Path = Path(data['mnt2'])
    backup2: Path = Path(data['backup2'])  # folder to backup to
    __daily: Path = backup2 / DIR_D
    if not __daily.exists():
        __daily.mkdir()
    __today: str = datetime.date.today().strftime('%y%m%d')
    __dpath = __daily / __today
    if __dpath.exists():
        logging.error(f"Dest '{__dpath}' already exists")
        return False
    __daily_are = __daily.iterdir()
    __yesterday: Path = sorted(__daily_are)[-1] if __daily_are else None
    # FIXME: must be < today
    for vh in data['vhost']:
        __vname = vh['name']  # guest registered name
        # # 1. stop vhost
        if os.getuid() == 0:
            logging.debug(f"Try to create vhost {__vname}")
            __vhost = virt.VHost(__vname)
            vstate0 = __vhost.State()
            if vstate0 == libvirt.VIR_DOMAIN_RUNNING:  # TODO: VIR_DOMAIN_PAUSED/VIR_DOMAIN_SHUTOFF
                retcode = __vhost.Suspend()  # TODO: process retcode
        for vd in vh['drive']:
            __vdrive = vdrive.VDrive(vd['path'], str(mnt2))
            for vp in vd['part']:
                __vdrive.mount(vp['dev'])
                for __dir in vp['dir']:
                    __type = __dir['type']
                    __sdir = __dir['path']
                    __spath = mnt2 / __sdir
                    if __type == 'rsync':
                        __rsync(__spath, __dpath, __yesterday)
                    elif __type == '1c7':
                        __7za(__spath, __dpath, '1[Cc][Vv]7.?[Dd] *.[Dd][Bb][Ff]')
                    elif __type == '1c8':
                        __7za(__spath, __dpath)
                    else:
                        logging.warning(f"Unknown type '{__type}' for path {__spath}")
                __vdrive.umount()
            # TODO: compress weekly/monthly
        # if vstate0 == libvirt.VIR_DOMAIN_RUNNING:
        #     __vhost.Resume()
    return True


def main():
    today = datetime.date.today()
    stoday = today.strftime('%y%m%d')
    data = pre.load_cfg('backup.json')
    log.setLogger(data.get('log'))
    if daily(data):  # FIXME: today arg
        rotate_dir(Path(data['backup2']) / DIR_D, 7)
        if today.weekday() == 6:  # sun => weekly
            cpal(Path(data['backup2']) / DIR_D / stoday, Path(data['backup2']) / DIR_W / stoday)
            rotate_dir(Path(data['backup2']) / DIR_W, 5)
            if today.day <= 7:  # monthly
                cpal(Path(data['backup2']) / DIR_D / stoday, Path(data['backup2']) / DIR_M / stoday)
                rotate_dir(Path(data['backup2']) / DIR_M, data.get('months', 3))
        # rsync_local()
        # backup_ftp()
        # backup_yadisk()
    # email()


if __name__ == '__main__':
    main()
