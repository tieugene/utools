"""Guest drive control.
os.path.ismount()
RTFM: https://github.com/vallentin/mount.py/blob/master/mount.py
"""


class VDrive(object):
    def __init__(self, path: str):
        ...

    def mount(self):
        ...

    def umount(self):
        ...
