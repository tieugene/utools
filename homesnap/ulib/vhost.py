"""KVM vhost control"""
# 2. 3rd
import libvirt
# 3. local
import exc


class VHost(object):
    state: int = None
    name: str = None
    __dom: libvirt.virDomain = None

    def __init__(self, name: str):
        self.name = name

    def getState(self):
        """Get vhost state.
        connection => domain => state
        TODO: commont try/exec block w/ libvirt exc handling
        RTFM: https://libvirt.org/docs/libvirt-appdev-guide-python/en-US/html/libvirt_application_development_guide_using_python-Guest_Domains-Information-State.html
        """
        try:
            conn = libvirt.openReadOnly(None)
        except libvirt.libvirtError:
            raise exc.YAPBKVMErrorError("Failed to open connection to the hypervisor")
        try:
            self.__dom = conn.lookupByName(self.name)
        except libvirt.libvirtError:
            raise exc.YAPBKVMErrorError("Failed to find the main domain")
        state, reason = self.__dom.state()  # [1, 5], [3, 1]
        if state not in {libvirt.VIR_DOMAIN_RUNNING, libvirt.VIR_DOMAIN_PAUSED, libvirt.VIR_DOMAIN_SHUTOFF}:
            raise exc.YAPBKVMErrorError("Vhost not run not paused nor shuted down")
        return state

    def Suspend(self):
        """Note: flush drives before"""
        try:
            self.__dom.suspend()
        except libvirt.libvirtError:
            raise exc.YAPBKVMErrorError("Cannot suspend")

    def Resume(self):
        """Resume vhost if it was running before"""
        try:
            self.__dom.resume()
        except libvirt.libvirtError:
            raise exc.YAPBKVMErrorError("Cannot resume")
