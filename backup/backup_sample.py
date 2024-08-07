#!/usr/bin/env python3
"""The main"""
# 1. std
import logging
import pathlib
import datetime
import sys
# 2. 3rds
# 3. local
from ulib import log, virt, backup, mail


LOG_LEVEL = logging.DEBUG
DIR_IMG = pathlib.Path('mnt/shares/images')
DIR_BACKUP = pathlib.Path('/mnt/shares/backup')
DIR_BACKUP_D = DIR_BACKUP / 'daily'
DIR_BACKUP_W = DIR_BACKUP / 'weekly'
DIR_BACKUP_M = DIR_BACKUP / 'monthly'
DIR_MNT = pathlib.Path('/mnt/tmp')
WEEKDAY = 6  # sunday; TODO: use .isoweekday() (mon=1, sun=7)
# vars
TODAY = datetime.date.today()
YMD = TODAY.strftime('%y%m%d')


def daily():
    logging.debug("Start daily")
    dir_today = DIR_BACKUP_D / YMD
    if dir_today.exists():
        # TODO: chk empty
        logging.info(f"%s already exists.", YMD)
        return True
    conn = virt.VConn()
    res = conn.open()  # FIXME: always OK (.opened); .list() is []
    dom = conn.get_vhost('winxp')
    state = dom.state()
    sys.exit()
    dailies = backup.dir_list(DIR_BACKUP_D)
    last = dailies[-1] if dailies else None
    backup.dir_mk(dir_today)
    if state == virt.DomState.Running:
        dom.suspend()
    backup.guest_mount('D')
    #   backup_dir 1
    #   backup_dir 2
    #   backup_1c7
    #   backup_1c8
    #   umount
    # mount E:
    #   backup_dir 3
    # if weekly:
    #   backup vdrives
    #   dump self
    # if state == virt.DomState.Running:
    #   start vm
    # conn.close()
    # dir_rotate(8)


def main():
    logging.basicConfig(level=LOG_LEVEL)
    try:
        daily()
        if TODAY.weekday() == WEEKDAY:
            backup.weekly(DIR_BACKUP_D, DIR_BACKUP_W, YMD, 8)  # == hlink+rotate
            if TODAY.day < 7:
                backup.monthly()  # == hlink+rotate
        backup.rsync_local()
    except (backup.UlibBackupError, virt.UlibVirtError) as e:
        logging.error(e)
    # mail.send_mail(result, ERRS)


if __name__ == '__main__':
    main()
