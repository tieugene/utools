#!/usr/bin/env python3
"""The main"""
# 1. std
import logging
import pathlib
import datetime
import sys
import traceback
# 2. 3rds
# 3. local
from ulib import exc, log, virt, backup, mail


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
    if backup.dir_exists(dir_today):
        # TODO: chk empty => rm
        logging.info(f"%s already exists.", YMD)
        return
    conn = virt.VConn()  # FIXME: always OK; .opened too; .list() is []
    conn.open()  # TOSO: with
    # TODO: chk .list() is empty
    dom = conn.get_vhost('winxp')  # TODO: with
    daylies = backup.dir_list(DIR_BACKUP_D)
    last = daylies[-1] if daylies else None
    backup.dir_mk(dir_today)
    sys.exit()
    if (state := dom.state()) == virt.DomState.Running:
        dom.suspend()
    sys.exit()
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
        if TODAY.weekday() == WEEKDAY:  # weekly
            backup.xly(DIR_BACKUP_D, DIR_BACKUP_W, YMD, 8)
            if TODAY.day < 7:  # monthly; FIXME: last sat of mon
                backup.xly(DIR_BACKUP_W, DIR_BACKUP_M, YMD, 6)
        # backup.rsync_local()
    except exc.UlibError as e:
        logging.error(e)  # FIXME: trace
        # logging.exception(e)
        # print(traceback.format_exc())
    # mail.send_mail(result, ERRS)


if __name__ == '__main__':
    main()
