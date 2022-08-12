#!/usr/bin/env python3
"""Backup.
Requires: rsync, 7za, zst, gustmount, gustunmount[, dump][, sudo, virsh]
Requires: python-libvirt (F34, RH8, ~CO7~)[, python-lxc (F34, RH8, ~CO7~)]
:todo: mail report queue
:todo: --dry-run
"""
# 1. std
import os
import datetime
import logging
import shutil
from pathlib import Path
# 2. 3rd
import libvirt
# 3. local
from ulib import exc, pre, log, sp, rsync, virt, vdrive

# x. const (TODO: to cfg | default)
DIR_D = 'daily'
DIR_W = 'weekly'
DIR_M = 'monthly'
WEEK_DAY = 7  # Sun
OPTS_7Z = ['-t7z', '-m0=lzma', '-mx=9', '-mfb=64', '-md=32m', '-ms=on']


class UlibBackupError(exc.UlibTextError):
    name = "Backup"


def __is_weekly(d: datetime.date):
    """Check it's time to weekly"""
    return d.isoweekday() == WEEK_DAY


def __is_monthly(d: datetime.date):
    """Check it's time to weekly"""
    return d.isoweekday() == WEEK_DAY and d.day <= 7


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


def zip_1c(spath: Path, dpath: Path, mask: str = '*') -> bool:
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


def zip_file(sfile: Path, ddir: Path):
    """Compress a file
    :param sfile: File to compress
    :param ddir: Dir to backup to
    :note: now zstd only
    """
    sp.sp(['zstd' '-k', '--output-dir-flat', sfile])


def cpal(sdir: Path, ddir: Path):
    """'cp -al src => dst"""
    sp.sp(['cp', '-al', sdir, ddir], UlibBackupError)


def rotate_dir(ddir: Path, size: int) -> bool:
    """Rotates folder content by given items"""
    if not ddir.is_dir():
        logging.error(f"Rotate: rotating dir '{ddir}' not found")
        return False
    for d in sorted(ddir.iterdir())[:-size]:
        if not d.is_dir():
            logging.warning(f"Rotate: '{d}' is not dir")
            continue
        print(f"Rmtree '{d}'")
        # shutil.rmtree(d)


def daily(data: dict, today: datetime.date) -> bool:
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
    __stoday: str = today.strftime('%y%m%d')
    __dpath = __daily / __stoday
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
                        zip_1c(__spath, __dpath, '1[Cc][Vv]7.?[Dd] *.[Dd][Bb][Ff]')
                    elif __type == '1c8':
                        zip_1c(__spath, __dpath)
                    else:
                        logging.warning(f"Unknown type '{__type}' for path {__spath}")
                __vdrive.umount()
            # TODO: compress weekly/monthly
            zip_period = vd.get('zip')
            if zip_period is None:
                pass
            elif (zip_period == 'd') or \
                    (zip_period == 'w' and __is_weekly(today)) or \
                    (zip_period == 'm' and __is_monthly(today)):
                zip_file(Path(vd['path']), __dpath)
            else:
                logging.warning(f"Unknown 'zip' period for {vd['path']}: {zip_period}")
        # if vstate0 == libvirt.VIR_DOMAIN_RUNNING:
        #     __vhost.Resume()
    return True


def main():
    data = pre.load_cfg('backup.json')
    log.setLogger(data.get('log'))
    today = datetime.date.today()
    if daily(data, today):  # FIXME: today arg
        rotate_dir(Path(data['backup2']) / DIR_D, 7)
        if __is_weekly(today):
            stoday = today.strftime('%y%m%d')
            cpal(Path(data['backup2']) / DIR_D / stoday, Path(data['backup2']) / DIR_W / stoday)
            rotate_dir(Path(data['backup2']) / DIR_W, 5)
            if __is_monthly(today):
                cpal(Path(data['backup2']) / DIR_D / stoday, Path(data['backup2']) / DIR_M / stoday)
                rotate_dir(Path(data['backup2']) / DIR_M, data.get('months', 3))
        # rsync_local()
        # backup_ftp()
        # backup_yadisk()
    # email()


if __name__ == '__main__':
    main()
