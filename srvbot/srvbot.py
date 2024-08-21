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
from typing import List, Dict, Set
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
LOG_LEVEL = logging.INFO
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


@dp.message(Command("start"))
async def on_start(message: types.Message):
    # TODO: check uid
    logging.info("Cmd 'start' from %d", message.from_user.id)
    await message.answer(_("Welcome.\nSend '/help' for list commands available."))


@dp.message(Command("help"))
async def on_help(message: types.Message):
    # start wrap
    if message.from_user.id not in ACL:
        logging.warning("UID %d not registered.")
        await message.answer(_("User unknown"))
        return
    # end wrap
    cmds = ACL[message.from_user.id].union({'start', 'help'})
    help_list = [f"/{k}: {v}" for k, v in HELP.items() if k in cmds]
    await message.answer("\n".join(help_list))


@dp.message(Command("active"))
async def on_active(message: types.Message):
    if message.from_user.id not in ACL:
        logging.warning("UID %d not registered.", message.from_user.id)
        await message.answer(_("User unknown"))
        return
    if 'active' not in ACL[message.from_user.id]:
        logging.warning("Command '%s' not permited for UID %d.", 'active', message.from_user.id)
        await message.answer(_("Access denied"))
        return
    try:
        # core
        answer = _("Active") if VConn.lookupByName(Settings.vhost).isActive() else _("Inactive")
        # /core
    except libvirt.libvirtError as e:
        answer = f"Error: {str(e)}"
    await message.answer(answer)


@dp.message(Command("state"))
async def on_state(message: types.Message):
    ...


@dp.message(Command("create"))
async def on_create(message: types.Message):
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
