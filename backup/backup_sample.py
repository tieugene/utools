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
- [ ] rsync_local => mount+rsync
- [ ] logging to str
- [ ] __force mode__
:note: [copy_stream](https://python-zstandard.readthedocs.io/en/latest/compressor.html)
"""
# 1. std
import logging
import pathlib
import datetime
import sys
import traceback
# 2. 3rds
# 3. local
from ulib import exc, log, virt, mnt, bckp, rsync, mail


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
    if bckp.dir_exists(DIR_BACKUP_2DAY):
        if bckp.dir_empty(DIR_BACKUP_2DAY):
            logging.debug("Rm %s", DIR_BACKUP_2DAY)
            bckp.dir_rm(DIR_BACKUP_2DAY)
        else:
            logging.info(f"%s already exists.", YMD)
            return
    prev = dailies[-1] if (dailies := bckp.dir_list(DIR_BACKUP_D)) else None
    conn = virt.VConn()
    conn.open()  # TODO: with
    # dom = conn.get_vhost('win7')  # TODO: with
    bckp.dir_mk(DIR_BACKUP_2DAY)
    # if (state := dom.state()) == virt.DomState.Running:
    #    dom.suspend()
    mnt.mount_guest(DIR_IMG / 'W7P_D.img', 1048576, DIR_MNT)
    bckp.backup_dir(DIR_MNT, DIR_BACKUP_2DAY, 'Public', prev)
    bckp.dir_mk(DIR_BACKUP_2DAY / '1C')
    bckp.backup_1c7(DIR_BACKUP / '1C' / '7', DIR_BACKUP_2DAY / '1C')
    bckp.backup_1c8(DIR_BACKUP / '1C' / '8', DIR_BACKUP_2DAY / '1C')
    mnt.umount(DIR_MNT)
    # mount E:
    #   backup_dir 3
    if TODAY.weekday() == WEEKDAY:
        bckp.backup_vdrive(DIR_IMG / 'W7P_D.img', DIR_BACKUP_2DAY)
        bckp.dump_self(DIR_BACKUP_2DAY / 'vms_root')
    # if state == virt.DomState.Running:
    #   dom.resume()
    conn.close()
    bckp.dir_rotate(DIR_BACKUP_D, 8)
    sys.exit()


def main():
    logging.basicConfig(level=LOG_LEVEL)
    try:
        daily()
        if TODAY.weekday() == WEEKDAY:  # weekly
            bckp.xly(DIR_BACKUP_D, DIR_BACKUP_W, YMD, 8)
            if TODAY.day < 7:  # monthly; FIXME: last weekly of mon
                bckp.xly(DIR_BACKUP_W, DIR_BACKUP_M, YMD, 6)
        # backup.rsync_local(pathlib.Path('/dev/sdb2'), DIR_MNT, DIR_BACKUP)
    except exc.UlibError as e:
        logging.error(e)  # FIXME: trace
        # logging.exception(e)
        # print(traceback.format_exc())
    # finally: umount
    # mail.send_mail(result, ERRS)


if __name__ == '__main__':
    main()
