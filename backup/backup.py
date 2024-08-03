"""The main"""
import socket
import sys
import datetime
# 3rds
# python-libvirt (F34, RH8, ~CO7~)
# python-lxc (F34, RH8, ~CO7~)
# local
from ulib import pre, log


ERRS: str = ''


class BackupError(RuntimeError):
    """Basic error"""
    msg: str

    def __init__(self, msg: str):
        super().__init__(self)
        self.msg = msg


def load_cfg() -> bool:
    try:
        data = pre.load_cfg('backup.ini')
        if data is None:
            sys.exit("Config not found")
    except pre.UlibCfgLoadError as e:
        sys.exit(str(e))


def monthly() -> bool:
    # std
    ...
    # if today.day <= 7:
    # cpal weekly
    # rotate


def weekly() -> bool:
    # std
    ...
    # if today.weekday == 6
    # pack vdisks, dump self
    # cpal daily
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
    # today = datetime.date.today()
    if load_cfg():  # std
        # debug_level = ...
        result = daily() & weekly() & monthly() & rsync_local()
        email(result, ERRS)
