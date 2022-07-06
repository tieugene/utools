"""KVM vhost control"""
# 1. std
from typing import List, Union
import functools
import logging
# 2. 3rd
import libvirt
# 3. local
from . import exc
# const
STATE_NAME = (
    "No state",
    "Running",
    "Blocked",
    "Paused",
    "ShutDown",
    "ShutOff",
    "Crashed",
    "PMSuspended"
)


class YAPBKVMErrorError(exc.YAPBTextError):
    """KVM error."""
    name = "Virt"


class VConn:
    """libvirt.virtConnect proxy"""
    __conn: libvirt.virConnect = None

    @staticmethod
    def conn() -> libvirt.virConnect:
        if not VConn.__conn:
            logging.debug("Try opening VConn")
            try:
                VConn.__conn = libvirt.open(None)  # localhost only
            except libvirt.libvirtError:
                raise YAPBKVMErrorError("Failed to open connection to the hypervisor")
        return VConn.__conn

    @staticmethod
    def list() -> List[int]:
        """:todo: shows all vhosts (listDefinedDomains())"""
        try:
            return VConn.conn().listDomainsID()
        except libvirt.libvirtError:
            raise YAPBKVMErrorError("Failed list vhosts")


def try_libvirt(reason: str):
    def decorator_try_libvirt(func: callable):
        @functools.wraps(func)
        def wrapper(ref) -> Union[int, bool]:
            try:
                return func(ref)
            except libvirt.libvirtError as e:
                raise YAPBKVMErrorError("%s (%s)" % (reason, str(e)))
        return wrapper
    return decorator_try_libvirt


class VHost(object):
    """libvirt.virtDomain proxy."""
    __dom: libvirt.virDomain = None

    def __init__(self, name: str):
        """:todo: lookupByID(int)"""
        try:
            self.__dom = VConn.conn().lookupByName(name)
        except libvirt.libvirtError as e:
            raise YAPBKVMErrorError("Cannot find vhost '%s' (%s)" % (name, str(e)))

    @try_libvirt("Cannot check vhost active")
    def isActive(self) -> bool:
        """Get vhost active.
        :return: True if active
        """
        return bool(self.__dom.isActive())

    @try_libvirt("Cannot get vhost state")
    def State(self) -> int:
        """Get vhost state.
        :return: 0 if OK
        """
        return self.__dom.state()[0]  # state, reason: [1, 5], [3, 1]

    @try_libvirt("Cannot create vhost")
    def Create(self) -> int:
        """Power on vhost
        :return: 0 if OK
        """
        return self.__dom.create()

    @try_libvirt("Cannot destroy vhost")
    def Destroy(self) -> int:
        """Power off vhost (hard)
        :return: 0 if OK
        """
        return self.__dom.destroy()

    @try_libvirt("Cannot suspend vhost")
    def Suspend(self) -> int:
        """Suspend vhost.
        :return: 0 if OK
        :todo: flush drives before
        """
        return self.__dom.suspend()

    @try_libvirt("Cannot resume vhost")
    def Resume(self) -> int:
        """Resume vhost after suspending.
        :return: 0 if OK
        """
        return self.__dom.resume()

    @try_libvirt("Cannot shutdown vhost")
    def ShutDown(self) -> int:
        """Shutdown vhost (soft)
        :return: 0 if OK
        """
        return self.__dom.shutdown()

    @try_libvirt("Cannot reboot vhost")
    def Reboot(self) -> int:
        """Reboot vhost (soft)
        :return: 0 if OK
        """
        return self.__dom.reboot()

    @try_libvirt("Cannot reset vhost")
    def Reset(self) -> int:
        """Reboot vhost (hard)
        :return: 0 if OK
        """
        return self.__dom.reset()
