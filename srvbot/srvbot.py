import asyncio
import gettext
import json
import logging
import os
import pathlib
from typing import Optional, List

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

LOG_LEVEL = logging.INFO
dp: Dispatcher = Dispatcher()


class SettingsType(BaseModel):
    class Acl(BaseModel):
        cmd: List[str]
        uid: List[int]

    model_config = ConfigDict(strict=True)
    log: int
    tglog: int
    token: str
    vhost: str
    acl: Optional[List[Acl]]


Settings: SettingsType


@dp.message(Command("start"))
async def on_start(message: types.Message):
    logging.info("Cmd start")
    await message.answer(_("Welcome.\nSend '/help' for list commands available."))


@dp.message(Command("help"))
async def on_start(message: types.Message):
    ...


@dp.message(Command("active"))
async def on_active(message: types.Message):
    ...


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


@dp.message(Command("list"))
async def on_list(message: types.Message):
    ...


async def on_default(message: types.Message):
    ...


def main():
    global Settings
    logging.basicConfig(level=LOG_LEVEL)
    cfg_fn = DIR / 'srvbot.json'
    with open(cfg_fn, 'rt') as i_f:
        data_dict = json.load(i_f)
        Settings = SettingsType(**data_dict)
    bot = Bot(token=Settings.token)
    asyncio.run(dp.start_polling(bot))


if __name__ == '__main__':
    main()
