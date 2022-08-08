"""The main"""
import sys
import datetime
import logging
# 3rds
# python-libvirt (F34, RH8, ~CO7~)
# python-lxc (F34, RH8, ~CO7~)
# local
from ulib import pre, log, virt, vdrive


class BackupError(RuntimeError):
    """Basic error"""
    msg: str

    def __init__(self, msg: str):
        super().__init__(self)
        self.msg = msg


def vm_start():
    ...


def vm_stop():
    ...


def lxc_start():
    ...


def lxc_stop():
    ...


def guest_mount():
    """libgustfs-tools-c(guestmount)"""
    ...


def guest_umount():
    """libgustfs-tools-c(guestmount)"""
    ...


def rsync():
    """rsync"""
    ...


def rotate():
    ...


def daily(data: dict):
    __vhost: virt.VHost = None
    mnt2 = data['mnt2']
    for vh in data['vhost']:
        vname = vh['name']
        logging.debug(f"Try to create vhost {vname}")
        #__vhost = virt.VHost(vname)
        # TODO: lxc
        # 1. stop vhost
        #vstate0 = __vhost.State()
        #if vstate0 == 1:  # running; TODO: paused (3)/shutoff(5)
        #    retcode = __vhost.Suspend()
        for vd in vh['drive']:
            __vdrive = vdrive.VDrive(vd['path'], mnt2)
            for vp in vd['part']:
                __vdrive.mount(vp['dev'])
                for __dir in vp['dir']:
                    print(__dir['path'], __dir['type'])
                __vdrive.umount()
        #__vhost.Resume()
    # rotate daily


def weekly():
    """cpal daily + dump/comp"""
    ...


def monthly():
    """cpall weekly"""
    ...


def main():
    # 1. load config
    try:
        data = pre.load_cfg('backup.json')
        if data is None:
            sys.exit("Config not found")
    except pre.UlibCfgLoadError as e:
        sys.exit(str(e))
    # 2. setup logger
    if 'log' in data:
        log.setLogger(data['log'])
    # 3. main
    today = datetime.date.today()
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
