#!/usr/bin/env python3
"""Telegram bot to handle KVM host.
:note: requires root permissions to control vhosts
:todo: default handler
"""
# 1. std
import asyncio
import gettext
import json
import logging
import os
import pathlib
from enum import unique, Enum
from typing import List, Dict, Set, Optional, Union
from dataclasses import dataclass
# 2. 3rd
import libvirt
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

DIR = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

# i18n
LOCALE_DIR = DIR / 'locale'
if not LOCALE_DIR.is_dir():  # default if in-place l10ns absent
    LOCALE_DIR = None
translate = gettext.translation('srvbot', localedir=str(LOCALE_DIR))
_ = translate.gettext

VConn: libvirt.virConnect
LOG_LEVEL = logging.DEBUG
dp: Dispatcher = Dispatcher()
ACL: Dict[int, Set[str]] = {}
HELP: Dict[str, str] = {
    "start": _("Start page"),
    "help": _("This page"),
    "state": _("State"),
    "suspend": _("Suspend"),
    "resume": _("Resume (after suspend)"),
    "create": _("Power on"),
    "reboot": _("Reboot"),
    "shutdown": _("Power off"),
    "reset": _("Reset (force reboot)"),
    "destroy": _("Power off (force)"),
    "active": _("Check is active"),
}
STATE_NAME = (
    _("No state"),
    _("Running"),
    _("Blocked"),
    _("Paused"),
    _("Shutdown"),
    _("Shutoff"),
    _("Crashed"),
    _("PM Suspended")
)

@unique
class Action(Enum):
    """Map of guest methods."""
    ACTIVE = 'isActive'  # int (0, 1)
    STATE = 'state'  # List[int, int]
    CREATE = 'create'  # int=0
    DESTROY = 'destroy'  # int=0
    SUSPEND = 'suspend'  # int=0
    RESUME = 'resume'  # int=0
    SHUTDOWN = 'shutdown'  # int=0
    REBOOT = 'reboot'  # int=0
    RESET = 'reset'  # int=0


@dataclass
class SettingsType:
    """Settings."""
    log: int
    tglog: int
    token: str
    vhost: str
    acl: List[Dict[str, List[Union[int, str]]]]

Settings: SettingsType


async def __chk_uid(message: types.Message) -> bool:
    """Check user registerd."""
    if message.from_user.id not in ACL:
        logging.warning("UID %d not registered.")
        await message.answer(_("User unknown"))
        return False
    logging.info("Cmd '%s', from %d", message.text, message.from_user.id)
    return True


@dp.message(Command("start"))
async def on_start(message: types.Message):
    """Start page."""
    if await __chk_uid(message):
        await message.answer(_("Welcome.\nSend '/help' for list commands available."))


@dp.message(Command("help"))
async def on_help(message: types.Message):
    """Help."""
    if await __chk_uid(message):
        cmds = ACL[message.from_user.id].union({'start', 'help'})
        help_list = [f"/{k}: {v}" for k, v in HELP.items() if k in cmds]
        await message.answer("\n".join(help_list))


async def __do_action(message: types.Message, meth: Action, quiet: bool = False)\
        -> Optional[Union[int, List[int]]]:
    """Check user registerd and command permited and dom ok."""
    uid = message.from_user.id
    cmd = message.text[1:]
    if uid not in ACL:
        logging.warning("UID %d not registered.", message.from_user.id)
        await message.answer(_("User unknown"))
    elif cmd not in ACL[message.from_user.id]:
        logging.warning("Command '%s' not permited for UID %d.", cmd, message.from_user.id)
        await message.answer(_("Access denied"))
    else:
        try:
            dom = VConn.lookupByName(Settings.vhost)
            f = getattr(dom, meth.value)
            result = f()
            # logging.debug("Result of %s is type %s == %s", message.text, type(result), result)
            if not quiet:
                return result
            await message.answer("OK")
        except libvirt.libvirtError as e:
            logging.error(str(e))
            await message.answer(f"Error: {str(e)}")


@dp.message(Command("active"))
async def on_active(message: types.Message):
    """Check guest is active (running, ...)."""
    if (is_active := await __do_action(message, Action.ACTIVE)) is not None:
        await message.answer( _("Active") if is_active else _("Inactive"))


@dp.message(Command("state"))
async def on_state(message: types.Message):
    """Get guest state."""
    if (state := await __do_action(message, Action.STATE)) is not None:
        await message.answer(STATE_NAME[state[0]])


@dp.message(Command("create"))
async def on_create(message: types.Message):
    """Start guest from scratch ('Power on')."""
    await __do_action(message, Action.CREATE, quiet=True)


@dp.message(Command("destroy"))
async def on_destroy(message: types.Message):
    """Power of guest (force)."""
    await __do_action(message, Action.DESTROY, quiet=True)


@dp.message(Command("suspend"))
async def on_suspend(message: types.Message):
    """Freeze guest."""
    await __do_action(message, Action.SUSPEND, quiet=True)


@dp.message(Command("resume"))
async def on_resume(message: types.Message):
    """Melt guest."""
    await __do_action(message, Action.RESUME, quiet=True)


@dp.message(Command("shutdown"))
async def on_shutdown(message: types.Message):
    """Power off (soft) guest."""
    await __do_action(message, Action.SHUTDOWN, quiet=True)


@dp.message(Command("reboot"))
async def on_reboot(message: types.Message):
    """Reboot (soft) guest."""
    await __do_action(message, Action.REBOOT, quiet=True)


@dp.message(Command("reset"))
async def on_reset(message: types.Message):
    """Reset (hard) guest."""
    await __do_action(message, Action.RESET, quiet=True)


def main():
    """CLI endpoint."""
    global Settings, VConn
    logging.basicConfig(level=LOG_LEVEL)
    cfg_fn = DIR / 'srvbot.json'
    with open(cfg_fn, 'rt', encoding='utf8') as i_f:
        data_dict = json.load(i_f)
        Settings = SettingsType(**data_dict)
        for acl in Settings.acl:  # permissions
            for uid in acl['uid']:
                ACL[uid] = set(acl['cmd'])
    bot = Bot(token=Settings.token)
    VConn = libvirt.open()  # ???
    asyncio.run(dp.start_polling(bot))


if __name__ == '__main__':
    main()
