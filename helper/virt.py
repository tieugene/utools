"""KVM vhost control"""
# 1. std
import functools
from typing import List
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


def try_libvirt(func: callable):
    @functools.wraps(func)
    def wrapper(ref, reason: str):
        try:
            return func(ref)
        except libvirt.libvirtError as e:
            raise YAPBKVMErrorError("%s (%s)" % (reason, str(e)))
    return wrapper


class VHost(object):
    """libvirt.virtDomain proxy.
    :todo: commont try/exec block w/ libvirt exc handling (decorator?)
    """
    __dom: libvirt.virDomain = None

    def __init__(self, name: str):
        """:todo: lookupByID(int)"""
        try:
            self.__dom = VConn.conn().lookupByName(name)
        except libvirt.libvirtError as e:
            raise YAPBKVMErrorError("Cannot find vhost '%s' (%s)" % (name, str(e)))

    @try_libvirt("Cannot check vhost active")
    def isActive(self) -> bool:
        """Get vhost active."""
        return bool(self.__dom.isActive())

    def State(self) -> int:
        """Get vhost state."""
        try:
            return self.__dom.state()[0]  # state, reason: [1, 5], [3, 1]
        except libvirt.libvirtError as e:
            raise YAPBKVMErrorError("Cannot get vhost state (%s)" % str(e))

    def Create(self) -> int:
        """Power on vhost"""
        try:
            return self.__dom.create()
        except libvirt.libvirtError as e:
            raise YAPBKVMErrorError("Cannot create vhost (%s)" % str(e))

    def Destroy(self) -> int:
        """Power off vhost (hard)"""
        try:
            return self.__dom.destroy()
        except libvirt.libvirtError as e:
            raise YAPBKVMErrorError("Cannot destroy vhost (%s)" % str(e))

    def Suspend(self) -> int:
        """Suspend vhost.
        :return: 0 if OK
        :todo: flush drives before
        """
        try:
            return self.__dom.suspend()
        except libvirt.libvirtError as e:
            raise YAPBKVMErrorError("Cannot suspend vhost (%s)" % str(e))

    def Resume(self) -> int:
        """Resume vhost after suspending
        :return: 0 if OK
        """
        try:
            return self.__dom.resume()
        except libvirt.libvirtError as e:
            raise YAPBKVMErrorError("Cannot resume vhost (%s)" % str(e))

    def ShutDown(self) -> int:
        """Shutdown vhost (soft)
        :return: 0 if OK
        """
        try:
            return self.__dom.shutdown()
        except libvirt.libvirtError as e:
            raise YAPBKVMErrorError("Cannot shutdown vhost (%s)" % str(e))

    def Reboot(self) -> int:
        """Reboot vhost (soft)
        :return: 0 if OK
        """
        try:
            return self.__dom.reboot()
        except libvirt.libvirtError as e:
            raise YAPBKVMErrorError("Cannot reboot vhost (%s)" % str(e))

    def Reset(self) -> int:
        """Reboot vhost (hard)
        :return: 0 if OK
        """
        try:
            return self.__dom.reset()
        except libvirt.libvirtError as e:
            raise YAPBKVMErrorError("Cannot reboot vhost (%s)" % str(e))
