"""The main"""
import socket
import sys
import datetime
# 3rds
# python-libvirt (F34, RH8, ~CO7~)
# python-lxc (F34, RH8, ~CO7~)
# local
from ulib import pre, log

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


def daily():
    ...


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
    # 2.
    today = datetime.date.today()
    daily()
    if today.weekday() == 6:  # sun
        weekly()
        if today.day <= 7:
            monthly()
    # rsync_local()
    # rsync_remote()
    # backup_ftp()
    # backup_yadisk()
    # email()
