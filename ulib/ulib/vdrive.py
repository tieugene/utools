"""Guest drive control.
RTFM: https://github.com/vallentin/mount.py/blob/master/mount.py
"""
# 1. std
import os
# 3. local
from . import exc, sp


class UlibVDriveError(exc.UlibTextError):
    """Config loading exceptions."""
    name = "VDrive"


class VDrive(object):
    __path: str
    __mnt2: str

    def __init__(self, path: str, mnt2: str):
        """
        :param path: vdrive image path
        :param mnt2: mount point
        :todo: chk path exists
        """
        self.__path = path
        self.__mnt2 = mnt2

    def mount(self, vpart: str):
        """
        :param vpart: virtual partition name (e.g. '/dev/sda1')
        """
        self.umount()
        sp.sp(['guestmount', '-a', self.__path, '-m', vpart, '--ro', self.__mnt2], UlibVDriveError)

    def umount(self):
        if os.path.ismount(self.__mnt2):
            sp.sp(['guestunmount', self.__mnt2], UlibVDriveError)
