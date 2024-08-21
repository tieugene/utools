#!/usr/bin/env python3
"""Telegram bot to handle KVM host.
Note: requires root permissions to control vhosts
"""
# 1. std
import asyncio
import gettext
import json
import logging
import os
import pathlib
from typing import List, Dict, Set, Optional
# 2. 3rd
import libvirt
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from pydantic import BaseModel, ConfigDict

DIR = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

# i18n
localedir = DIR / 'locale'
if not localedir.is_dir():  # default if in-place l10ns absent
    localedir = None
translate = gettext.translation('srvbot', localedir=str(localedir))
_ = translate.gettext

Settings: 'SettingsType'
VConn: libvirt.virConnect
LOG_LEVEL = logging.DEBUG
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
dp: Dispatcher = Dispatcher()


class SettingsType(BaseModel):
    class Acl(BaseModel):
        uid: List[int]
        cmd: List[str]

    model_config = ConfigDict(strict=True)
    log: int
    tglog: int
    token: str
    vhost: str
    acl: List[Acl]


async def __chk_uid(message: types.Message) -> bool:
    """Check user registerd."""
    if message.from_user.id not in ACL:
        logging.warning("UID %d not registered.")
        await message.answer(_("User unknown"))
        return False
    logging.info("Cmd '%s', from %d", message.text, message.from_user.id)
    return True


async def __chk_acl(message: types.Message) -> Optional[libvirt.virDomain]:
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
            return VConn.lookupByName(Settings.vhost)
        except libvirt.libvirtError as e:
            await message.answer(f"Error: {str(e)}")


@dp.message(Command("start"))
async def on_start(message: types.Message):
    if await __chk_uid(message):
        await message.answer(_("Welcome.\nSend '/help' for list commands available."))


@dp.message(Command("help"))
async def on_help(message: types.Message):
    if await __chk_uid(message):
        cmds = ACL[message.from_user.id].union({'start', 'help'})
        help_list = [f"/{k}: {v}" for k, v in HELP.items() if k in cmds]
        await message.answer("\n".join(help_list))


@dp.message(Command("active"))
async def on_active(message: types.Message):
    if dom := await __chk_acl(message):
        try:
            # core
            await message.answer( _("Active") if dom.isActive() else _("Inactive"))
            # /core
        except libvirt.libvirtError as e:
            await message.answer(f"Error: {str(e)}")


@dp.message(Command("state"))
async def on_state(message: types.Message):
    if dom := await __chk_acl(message):
        await message.answer(STATE_NAME[dom.state()[0]])


@dp.message(Command("create"))
async def on_create(message: types.Message):
    """"""
    ...


@dp.message(Command("destroy"))
async def on_destroy(message: types.Message):
    ...


@dp.message(Command("suspend"))
async def on_suspend(message: types.Message):
    ...


@dp.message(Command("resume"))
async def on_resume(message: types.Message):
    ...


@dp.message(Command("shutdown"))
async def on_shutdown(message: types.Message):
    ...


@dp.message(Command("reboot"))
async def on_reboot(message: types.Message):
    ...


@dp.message(Command("reset"))
async def on_reset(message: types.Message):
    ...


async def on_default(message: types.Message):
    ...


def main():
    global Settings, VConn
    logging.basicConfig(level=LOG_LEVEL)
    cfg_fn = DIR / 'srvbot.json'
    with open(cfg_fn, 'rt') as i_f:
        data_dict = json.load(i_f)
        Settings = SettingsType(**data_dict)
        for acl in Settings.acl:  # permissions
            for uid in acl.uid:
                ACL[uid] = set(acl.cmd)
    bot = Bot(token=Settings.token)
    VConn = libvirt.open()  # ???
    asyncio.run(dp.start_polling(bot))


if __name__ == '__main__':
    main()
