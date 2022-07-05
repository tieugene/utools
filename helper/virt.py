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
    """libvirt.virtDomain proxy"""
    state: int = None
    __dom: libvirt.virDomain = None

    def __init__(self, name: str):
        """:todo: lookupByID(int)"""
        try:
            self.__dom = VConn.conn().lookupByName(name)
        except libvirt.libvirtError:
            raise exc.YAPBKVMErrorError("Failed to find the main domain")

    def State(self) -> int:
        """Get vhost state.
        connection => domain => state
        TODO: commont try/exec block w/ libvirt exc handling
        RTFM: https://libvirt.org/docs/libvirt-appdev-guide-python/en-US/html/libvirt_application_development_guide_using_python-Guest_Domains-Information-State.html
        """
        state, reason = self.__dom.state()  # [1, 5], [3, 1]
        if state not in {libvirt.VIR_DOMAIN_RUNNING, libvirt.VIR_DOMAIN_PAUSED, libvirt.VIR_DOMAIN_SHUTOFF}:
            raise exc.YAPBKVMErrorError("Vhost not run not paused nor shuted down")
        return state

    def Suspend(self):
        """Note: flush drives before"""
        try:
            return self.__dom.suspend()
        except libvirt.libvirtError:
            raise exc.YAPBKVMErrorError("Cannot suspend")

    def Resume(self):
        """Resume vhost if it was running before"""
        try:
            return self.__dom.resume()
        except libvirt.libvirtError:
            raise exc.YAPBKVMErrorError("Cannot resume")
