"""KVM vhost control
:todo: add logger"""
# 2. 3rd
import libvirt
# 3. local
from . import exc


class VConn(object):
    """libvirt.virtConnect proxy"""
    __conn = None  # : libvirt.virtConnect

    def __init__(self):
        try:
            self.__conn = libvirt.openReadOnly(None)  # localhost only
        except libvirt.libvirtError:
            raise exc.YAPBKVMErrorError("Failed to open connection to the hypervisor")

    @property
    def conn(self):  # -> libvirt.virtConnect:
        return self.__conn

    def vlist(self):  # -> list[id]:
        try:
            return self.__conn.listDomainsID()
        except libvirt.libvirtError:
            raise exc.YAPBKVMErrorError("Failed vlist vhosts")


class VHost(object):
    """libvirt.virtDomain proxy"""
    state: int = None
    __dom = None  # : libvirt.virDomain = None

    def __init__(self, vconn: VConn, name: str):
        """:todo: lookupByID(int)"""
        try:
            self.__dom = vconn.conn.lookupByName(name)
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
