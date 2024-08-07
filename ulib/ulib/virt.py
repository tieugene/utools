"""KVM vhost control"""
# python-libvirt (F34, RH8, ~CO7~)
# python-lxc (F34, RH8, ~CO7~)
from enum import IntEnum, unique, auto
# 1. std
from typing import List, Union, Optional
import functools
import logging
# 2. 3rd
import libvirt
# 3. local
from . import exc


class UlibVirtError(exc.UlibTextError):
    """KVM error."""
    name = "Virt"


@unique
class DomState(IntEnum):
    No_state = 0
    Running = 1
    Blocked = 2
    Paused = 3
    Shutdown = 4
    Shutoff = 5
    Crashed = 6
    Suspended = 7


@unique
class DomAction(IntEnum):
    CREATE = auto()
    DESTROY = auto()
    SUSPEND = auto()
    RESUME = auto()
    SHUTDOWN = auto()
    REBOOT = auto()
    RESET = auto()


class VHost(object):
    """libvirt.virtDomain proxy."""
    __dom: Optional[libvirt.virDomain]

    def __init__(self, dom: libvirt.virDomain):
        """:todo: lookupByID(int)"""
        self.__dom = dom

    def is_active(self) -> bool:
        """Get vhost active.
        :return: True if active
        """
        return bool(self.__dom.isActive())

    def state(self) -> DomState:
        """Get vhost state.
        :return: 0 if OK
        state, reason:
        - [5, 0]: off
        - [1, 5]: run, resume
        - [3, 1]: suspended
        """
        return DomState(self.__dom.state()[0])

    def create(self) -> int:
        """Power on vhost
        :return: 0 if OK
        """
        return self.__dom.create()

    def destroy(self) -> int:
        """Power off vhost (hard)
        :return: 0 if OK
        """
        return self.__dom.destroy()

    def suspend(self) -> int:
        """Suspend vhost.
        :return: 0 if OK
        :todo: flush drives before
        """
        return self.__dom.suspend()

    def resume(self) -> int:
        """Resume vhost after suspending.
        :return: 0 if OK
        """
        return self.__dom.resume()

    def shut_down(self) -> int:
        """Shutdown vhost (soft)
        :return: 0 if OK
        """
        return self.__dom.shutdown()

    def reboot(self) -> int:
        """Reboot vhost (soft)
        :return: 0 if OK
        """
        return self.__dom.reboot()

    def reset(self) -> int:
        """Reboot vhost (hard)
        :return: 0 if OK
        """
        return self.__dom.reset()


class VConn:
    """libvirt.virtConnect proxy"""
    __conn: Optional[libvirt.virConnect]

    def __init__(self):
        self.__conn = None

    def open(self) -> bool:
        """Open libvirtd connection.
        :exceptions:
        - libvirt not running
        - access denied
        :fixme: always ok
        """
        if self.__conn is None:
            try:
                logging.debug("Try to open connection")
                self.__conn = libvirt.open()  # localhost only
                logging.debug("Seems connected.")
            except libvirt.libvirtError:
                raise UlibVirtError("Failed to open connection to the hypervisor")
            if not self.__conn:
                logging.debug("Connect is None")
                self.__conn = None
        return bool(self.__conn)

    @property
    def opened(self) -> bool:
        return bool(self.__conn)

    def close(self):
        if self.__conn:
            if self.__conn.close():
                self.__conn = None

    def list(self) -> List[str]:
        """List vhosts.
        :exceptions:
        - not connected
        - access denied
        """
        try:
            return self.__conn.listDefinedDomains()
        except libvirt.libvirtError:
            raise UlibVirtError("Failed list vhosts")

    def get_vhost(self, name: str) -> VHost:
        """
        :exceptions:
        - not connected
        - dom not found
        - access denied
        """
        try:
            return VHost(self.__conn.lookupByName(name))
        except libvirt.libvirtError as e:
            raise UlibVirtError("Cannot find vhost '%s' (%s)" % (name, str(e)))


def try_libvirt(reason: str):
    # usage: @try_libvirt("Cannot check vhost active")
    def decorator_try_libvirt(func: callable):
        @functools.wraps(func)
        def wrapper(ref) -> Union[int, bool]:
            try:
                return func(ref)
            except libvirt.libvirtError as e:
                raise UlibVirtError("%s (%s)" % (reason, str(e)))
        return wrapper
    return decorator_try_libvirt
