"""The main"""
import socket
import sys
import pathlib
import datetime
# 3rds
# local
from ulib import pre, log


ERRS: str = ''
DIR_IMG = pathlib.Path('mnt/shares/images')
DIR_BACKUP = pathlib.Path('/mnt/shares/backup')
DIR_MNT = pathlib.Path('/mnt/tmp')


class BackupError(RuntimeError):
    """Basic error"""
    msg: str

    def __init__(self, msg: str):
        super().__init__(self)
        self.msg = msg


def monthly() -> bool:
    # std
    ...
    # if today.day <= 7:
    # cpal/hardlink weekly
    # rotate


def weekly() -> bool:
    # std
    ...
    # if today.weekday == 6
    # pack vdisks, dump self
    # cpal/hardlink daily
    # rotate


def daily() -> bool:
    # UDF
    ...
    # mk dir
    # connect libvirt
    # stop vm
    # mount D:
    #   backup_dir 1
    #   backup_dir 2
    #   backup_1c7
    #   backup_1c8
    #   umount
    # mount E:
    #   backup_dir 3
    # start vm
    # rotate


def main():
    # debug_level = ...
    today = datetime.date.today()
    dst = today.strftime('%y%m%d')
    result = daily() & weekly() & monthly() & rsync_local()
    mail.send_mail(result, ERRS)
