#!/usr/bin/env python3
"""Telegram bot to handle KVM host.
:todo: handle_x into decorator
:todo: auth
"""
# 1. std
import enum
import sys
import logging
# 2. 3rd
# noinspection PyPackageRequirements
import telebot
# 3. local
from helper import pre, log, virt

# const
ACL_LEVELS = 4  # 0..3
CHECK = '✓'
WELCOME = "Welcome.\nSend '/help' for list available commends."
HELP = '''/help: this page
/active: Check whether is running
/state: Get status
/run: Run
/suspend: Suspend
/resume: Resume after suspend
/reboot: Reboot (soft)
/reset: Reset (hard)
/shutdown: Shutdown (soft)
/poweroff: Power Off (hard)
/list: list all vhosts'''

# var
data: dict  # loaded config
bot: telebot.TeleBot  # bot itself
vhost: virt.VHost = None  # the vhost whto control to
acl: dict = {}  # user.id -> ACL level
help_text: list = []  # separate for each ACL level


class IEACLevel(enum.IntEnum):
    Admin = 0
    Private = 1
    Protected = 2
    Public = 3


class CanUse(telebot.custom_filters.SimpleCustomFilter):
    key = 'can_use'

    @staticmethod
    def check(message: telebot.types.Message) -> bool:
        logging.debug("can_use: " + message.text)
        return message.from_user.id == 798758379


def __try_vhost() -> virt.VHost:
    global vhost
    if not vhost:
        logging.debug("Try to create vhost")
        vhost = virt.VHost(data['vhost'])
    return vhost


def on_start(message):
    bot.reply_to(message, WELCOME)


def on_help(message):
    bot.reply_to(message, HELP)


def on_active(message):
    try:
        responce = "Active: " + ('✗', CHECK)[int(__try_vhost().isActive())]
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def on_state(message):
    try:
        state = __try_vhost().State()
        responce = "State: %d (%s)" % (state, virt.STATE_NAME[state])
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def on_create(message):
    try:
        retcode = __try_vhost().Create()
        logging.debug(type(retcode))
        responce = "Start: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def on_destroy(message):
    try:
        retcode = __try_vhost().Destroy()
        logging.debug(type(retcode))
        responce = "Destroy: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def on_suspend(message):
    try:
        retcode = __try_vhost().Suspend()
        logging.debug(type(retcode))
        responce = "Suspend: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def on_resume(message):
    try:
        retcode = __try_vhost().Resume()
        logging.debug(type(retcode))
        responce = "Resume: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def on_shutdown(message):
    try:
        retcode = __try_vhost().ShutDown()
        logging.debug(type(retcode))
        responce = "Shutdown: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def on_reboot(message):
    try:
        retcode = __try_vhost().Reboot()
        logging.debug(type(retcode))
        responce = "Reboot: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def on_reset(message):
    try:
        retcode = __try_vhost().Reset()
        logging.debug(type(retcode))
        responce = "Reset: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def on_list(message):
    try:
        responce = "VList: %s" % ', '.join(map(str, virt.VConn.list()))
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


HANDLERS = {
    # TODO: mk help from this
    # TODO: key: (func, desc, min ACL lvl)
    "start": on_start,
    "help": on_help,
    "active": on_active,
    "state": on_state,
    "run": on_create,
    "suspend": on_suspend,
    "resume": on_resume,
    "reboot": on_reboot,
    "reset": on_reset,
    "shutdown": on_shutdown,
    "poweroff": on_destroy,
    "list": on_list,
}


def main():
    """Main procedure."""
    global data, bot
    # 1. load cfg
    try:
        data = pre.load_cfg('srvbot.json')
        if data is None:
            sys.exit("Config not found")
    except pre.YAPBCfgLoadError as e:
        sys.exit(str(e))
    # 2. setup logger
    log.setLogger(data.get('log', 5))
    if 'tglog' in data:
        # logger = telebot.logger
        telebot.logger.setLevel(data['tglog'])  # 0: NOTSET, 10: DEBUG, ..., 50: CRITICAL
    # 3. setup tg-bot
    bot = telebot.TeleBot(data['bot']['token'], parse_mode=None)
    for k, v in HANDLERS.items():
        bot.register_message_handler(v, commands=[k] if isinstance(k, str) else list(k))
    # 4. go
    bot.infinity_polling()


if __name__ == '__main__':
    main()
