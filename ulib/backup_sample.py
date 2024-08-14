#!/usr/bin/env python3
"""The main.
:TODO:
- [..] backup_dir (=> rsync)
- [..] backup_1c7 => zipfile
- [..] backup_1cv8 => zstd(file)
- [..] pack_vdrive => zstd(file)
- [.] dump => sh.dump
- [.] backup.dir_rotate
- [.] backup.xly
- [.] rsync_local => mount+rsync
- [ ] logging
- [.] log 2 str
"""
# 1. std
import logging
import pathlib
import datetime
import sys
import traceback
# 2. 3rds
# 3. local
from ulib import exc, log, virt, mnt, bckp, rsync, mail, pth


LOG_LEVEL = logging.DEBUG
DIR_IMG = pathlib.Path('/mnt/shares/images')
DIR_BACKUP = pathlib.Path('/mnt/shares/backup')
DIR_MNT = pathlib.Path('/mnt/tmp')
WEEKDAY = 7  # sunday
# vars
DIR_BACKUP_D = DIR_BACKUP / 'daily'
DIR_BACKUP_W = DIR_BACKUP / 'weekly'
DIR_BACKUP_M = DIR_BACKUP / 'monthly'
TODAY = datetime.date.today()
YMD = TODAY.strftime('%y%m%d')
DIR_BACKUP_2DAY = DIR_BACKUP_D / YMD


def daily():
    logging.debug("Start daily")
    if pth.exists(DIR_BACKUP_2DAY):
        if pth.dir_empty(DIR_BACKUP_2DAY):
            logging.debug("Rm %s", DIR_BACKUP_2DAY)
            pth.dir_rm(DIR_BACKUP_2DAY)
        else:
            logging.info(f"%s already exists.", YMD)
            return
    prev = dailies[-1] if (dailies := pth.dir_list(DIR_BACKUP_D)) else None
    conn = virt.VConn()
    conn.open()  # TODO: with
    dom = conn.get_vhost('win7')  # TODO: with
    pth.dir_mk(DIR_BACKUP_2DAY)
    if (state := dom.state()) == virt.DomState.Running:
        dom.suspend()
    mnt.mount_guest(DIR_IMG / 'W7P_D.img', 1048576, DIR_MNT)
    bckp.backup_dir(DIR_MNT, DIR_BACKUP_2DAY, 'Public', prev)
    pth.dir_mk(DIR_BACKUP_2DAY / '1C')
    bckp.backup_1c7(DIR_BACKUP / '1C' / '7', DIR_BACKUP_2DAY / '1C')
    bckp.backup_1c8(DIR_BACKUP / '1C' / '8', DIR_BACKUP_2DAY / '1C')
    mnt.umount(DIR_MNT)
    # mount E:
    #   backup_dir 3
    if TODAY.weekday() == WEEKDAY:
        bckp.backup_vdrive(DIR_IMG / 'W7P_D.img', DIR_BACKUP_2DAY)
        bckp.dump_self(DIR_BACKUP_2DAY / 'vms_root')
    if state == virt.DomState.Running:
        dom.resume()
    conn.close()
    pth.dir_rotate(DIR_BACKUP_D, 8)


def main():
    log_str = log.set_logger(logging.DEBUG, with_str=True)
    try:
        daily()
        if TODAY.isoweekday() == WEEKDAY:  # weekly
            bckp.xly(DIR_BACKUP_2DAY, DIR_BACKUP_W, 8)
            if TODAY.day > (bckp.ldom(TODAY) - 7):  # monthly
                bckp.xly(DIR_BACKUP_W / YMD, DIR_BACKUP_M, 6)
        # bckp.rsync_local(pathlib.Path('/dev/sdb2'), DIR_MNT, DIR_BACKUP)
        result = True
    except exc.UlibError as e:
        logging.error(e)  # FIXME: trace
        result = False
        # logging.exception(e)
        # print(traceback.format_exc())
    # finally: umount
    print(log_str.getvalue())
    sys.exit()
    mail.send_mail(
        smtp='smtp.yandex.ru',
        mailfrom='Robot <robot@example.com>',
        creditentials=('robot@example.com', 'password'),
        mailto='admin@example.com',
        subj='Backup ' + ('OK' if result else 'ERR'),
        body=log_str.getvalue()
    )


if __name__ == '__main__':
    main()
