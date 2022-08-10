#!/usr/bin/env python3
"""Backup"""
# 1. std
import os
import datetime
import logging
from pathlib import Path
# 32. rds
# python-libvirt (F34, RH8, ~CO7~)
# python-lxc (F34, RH8, ~CO7~)
import libvirt
# 3. local
from ulib import exc, pre, log, rsync, virt, vdrive
# x. const (TODO: to cfg | default)
DIR_D = 'daily'
DIR_W = 'weekly'
DIR_M = 'monthly'


class UlibBackupError(exc.UlibTextError):
    """Config loading exceptions."""
    name = "Backup"


def __rsync(spath: Path, dpath: Path, by: Path = None):
    """rsync
    :param spath: Abs source path to backup
    :param dpath: Abs dest path ('/…/YYMMDD')
    :param by: Abs prev path ('yesterday', '/…/YYMMDD')
    """
    # chk prev exists
    # resolve prev against today
    # print(spath, dpath, by)
    if not spath.is_dir():
        raise UlibBackupError(f"Source dir '{spath}' not found")
    __tail = spath.name
    __dest = dpath / __tail
    if __dest.exists():
        raise UlibBackupError(f"Dest '{__dest}' already exists")
    opts = ['-axAXH', '--modify-window=1', '--del']
    __prev = by / __tail
    if not __prev.is_dir():
        logging.warning(f"Prev dir '{__prev}' not found")
    else:
        opts.append(f"--link-dest={os.path.relpath(__prev, __dest)}")
    opts.extend([str(spath) + '/', str(__dest)])
    dpath.mkdir(exist_ok=True)
    # print(' '.join(cmds))
    rsync.rsync(opts)


def __7za(spath: Path, dpath: Path):
    ...


def rotate():
    ...


def daily(data: dict):
    """Daily tasks.
    :todo: lxc guest
    :todo: force backup flag
    """
    mnt2: Path = Path(data['mnt2'])
    backup2: Path = Path(data['backup2'])  # folder to backup to
    __daily: Path = backup2 / DIR_D
    __today: str = datetime.date.today().strftime('%y%m%d')
    __dpath = __daily / __today
    if __dpath.exists():
        raise UlibBackupError(f"Dest '{__dpath}' already exists")
    __daily_are = __daily.iterdir()
    __yesterday: Path = sorted(__daily_are)[-1] if __daily_are else None
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
                    elif __type == '7za':
                        __7za(__spath, __dpath)
                    else:
                        logging.warning(f"Unknown type '{__type}' for path {__spath}")
                __vdrive.umount()
            # TODO: compress weekly/monthly
        # if vstate0 == libvirt.VIR_DOMAIN_RUNNING:
        #     __vhost.Resume()
    # rotate daily


def weekly():
    """cpal daily + dump/comp + rotate"""
    # cpal daily
    # rotate weekly


def monthly():
    """cpall weekly"""
    # cpal weekly
    # rotate monthly


def main():
    today = datetime.date.today()
    # 1. load config
    data = pre.load_cfg('backup.json')
    # 2. setup logger
    log.setLogger(data.get('log'))
    # 3. main
    daily(data)
    if today.weekday() == 6:  # sun
        weekly()
        if today.day <= 7:
            monthly()
    # rsync_local()
    # rsync_remote()
    # backup_ftp()
    # backup_yadisk()
    # email()


if __name__ == '__main__':
    main()
