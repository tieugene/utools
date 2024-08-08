#!/usr/bin/env python3
"""The main.
:TODO:
- [ ] backup_dir => rsync
- [ ] backup_1cX => 7za
- [ ] pack_vdir => 7za
- [ ] dump => sh.dump
- [ ] rsync_local => rsync
"""
# 1. std
import logging
import pathlib
import datetime
import sys
import traceback
# 2. 3rds
# 3. local
from ulib import exc, log, virt, mnt, backup, rsync, mail


LOG_LEVEL = logging.DEBUG
DIR_IMG = pathlib.Path('/mnt/shares/images')
DIR_BACKUP = pathlib.Path('/mnt/shares/backup')
DIR_MNT = pathlib.Path('/mnt/tmp')
WEEKDAY = 6  # sunday; TODO: use .isoweekday() (mon=1, sun=7)
# vars
DIR_BACKUP_D = DIR_BACKUP / 'daily'
DIR_BACKUP_W = DIR_BACKUP / 'weekly'
DIR_BACKUP_M = DIR_BACKUP / 'monthly'
TODAY = datetime.date.today()
YMD = TODAY.strftime('%y%m%d')
DIR_BACKUP_2DAY = DIR_BACKUP_D / YMD


def daily():
    logging.debug("Start daily")
    if backup.dir_exists(DIR_BACKUP_2DAY):
        if backup.dir_empty(DIR_BACKUP_2DAY):
            logging.debug("Rm")
            backup.dir_rm(DIR_BACKUP_2DAY)
        else:
            logging.info(f"%s already exists.", YMD)
            return
    dailies = backup.dir_list(DIR_BACKUP_D)
    prev = dailies[-1] if dailies else None
    conn = virt.VConn()
    conn.open()  # TODO: with
    # dom = conn.get_vhost('winxp')  # TODO: with
    backup.dir_mk(DIR_BACKUP_2DAY)
    # if (state := dom.state()) == virt.DomState.Running:
    #    dom.suspend()
    mnt.mount_guest(DIR_IMG / 'WXP_D.img', 32256, DIR_MNT)
    backup.backup_dir(DIR_MNT, DIR_BACKUP_2DAY, 'Public', prev)
    #   backup_1c7
    #   backup_1c8
    mnt.umount(DIR_MNT)
    # mount E:
    #   backup_dir 3
    # if weekly:
    #   backup vdrives
    #   dump self
    # if state == virt.DomState.Running:
    #   start vm
    conn.close()
    # dir_rotate(8)
    sys.exit()


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
    # finally: umount
    # mail.send_mail(result, ERRS)


if __name__ == '__main__':
    main()
