"""The main"""
import socket
import sys
import datetime
import logging
import logging.handlers
# 3rds
# python-libvirt (F34, RH8, ~CO7~)
# python-lxc (F34, RH8, ~CO7~)

# local
from . import const


class BackupError(RuntimeError):
    """Basic error"""
    msg: str

    def __init__(self, msg: str):
        super().__init__(self)
        self.msg = msg


def get_lock(process_name):
    """
    [pid](https://pypi.org/project/pid/), F34 ok
    [pidfile](https://pypi.org/project/python-pidfile/)
    Not required. Systemd did it
    https://stackoverflow.com/a/7758075/13294736
    """
    get_lock._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    try:
        get_lock._lock_socket.bind('\0' + process_name)
    except socket.error:
        sys.exit()


def load_config():
    ...


def log_open():
    """Open logger
    :todo: handle loglevel
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s(SMS): %(msg)s",
        handlers=(
            logging.StreamHandler(),
            logging.handlers.SysLogHandler(
                address='/var/run/syslog' if sys.platform == 'darwin' else '/dev/log'
            )
        )
    )


def log():
    """logging"""
    ...


def vm_start():
    ...


def vm_stop():
    ...


def lxc_stop():
    ...


def lxc_start():
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
    get_lock(const.NAME)
    log_open()
    load_config()
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
