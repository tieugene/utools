"""KVM vhost control
:todo: add logger"""
# 1. std
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
                raise exc.YAPBKVMErrorError("Failed to open connection to the hypervisor")
        return VConn.__conn

    @staticmethod
    def vlist() -> List[int]:
        """:todo: shows all vhosts (listDefinedDomains())"""
        try:
            return VConn.conn().listDomainsID()
        except libvirt.libvirtError:
            raise exc.YAPBKVMErrorError("Failed vlist vhosts")


class VHost(object):
    """libvirt.virtDomain proxy.
    :todo: commont try/exec block w/ libvirt exc handling (decorator?)
    """
    state: int = None
    __dom: libvirt.virDomain = None

    def __init__(self, name: str):
        """:todo: lookupByID(int)"""
        try:
            self.__dom = VConn.conn().lookupByName(name)
        except libvirt.libvirtError as e:
            raise exc.YAPBKVMErrorError("Cannot find vhost '%s' (%s)" % (name, str(e)))

    def isActive(self) -> bool:
        """Get vhost active."""
        try:
            return bool(self.__dom.isActive())
        except libvirt.libvirtError as e:
            raise exc.YAPBKVMErrorError("Cannot check vhost active (%s)" % str(e))

    def State(self) -> int:
        """Get vhost state."""
        try:
            return self.__dom.state()[0]  # state, reason: [1, 5], [3, 1]
        except libvirt.libvirtError as e:
            raise exc.YAPBKVMErrorError("Cannot get vhost state (%s)" % str(e))

    def Suspend(self):
        """Note: flush drives before"""
        try:
            return self.__dom.suspend()
        except libvirt.libvirtError as e:
            raise exc.YAPBKVMErrorError("Cannot suspend vhost (%s)" % str(e))

    def Resume(self):
        """Resume vhost if it was running before"""
        try:
            return self.__dom.resume()
        except libvirt.libvirtError as e:
            raise exc.YAPBKVMErrorError("Cannot resume vhost (%s)" % str(e))
