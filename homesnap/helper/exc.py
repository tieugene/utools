"""Exceptions.
RTFM: https://libvirt.org/docs/libvirt-appdev-guide-python/en-US/html/libvirt_application_development_guide_using_python-Error_Handling.html
"""


class YAPBError(RuntimeError):
    """Basic error"""
    ...


class YAPBTextError(YAPBError):
    """Exception with a text msg"""
    name: str
    msg: str

    def __init__(self, msg: str):
        super().__init__(self)
        self.msg = msg

    def __str__(self):
        return f"{self.name} error: {self.msg}"


class YAPBKVMErrorError(YAPBTextError):
    """KVM error"""
