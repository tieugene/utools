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
# var
data: dict  # loaded config
bot: telebot.TeleBot  # bot itself
vhost: virt.VHost = None  # the vhost whto control to
user_acl: dict = {}  # user.id -> ACL level
cmd_acl: dict = {}   # cmd -> ACL level
help_text: list = [[], [], [], []]  # separate for each ACL level


class IEACLevel(enum.IntEnum):
    Admin = 0
    Private = 1
    Protected = 2
    Public = 3


class CanUse(telebot.custom_filters.SimpleCustomFilter):
    key = 'can_use'

    @staticmethod
    def check(message: telebot.types.Message) -> bool:
        uid = message.from_user.id
        cmd = message.text
        logging.debug("can_use: uid=%d, cmd=%s" % (uid, cmd))
        return True


def __try_vhost() -> virt.VHost:
    global vhost
    if not vhost:
        logging.debug("Try to create vhost")
        vhost = virt.VHost(data['vhost'])
    return vhost


def on_start(message):
    bot.send_message(message.chat.id, WELCOME)


def on_help(message):
    uid = message.from_user.id
    u_acl = user_acl[uid]
    help_txt = help_text[u_acl]
    logging.debug("Help: uid=%d, acl=%d" % (uid, u_acl))
    # print(help_txt)
    bot.send_message(message.chat.id, '\n'.join(help_txt))


def on_active(message):
    try:
        responce = "Active: " + ('✗', CHECK)[int(__try_vhost().isActive())]
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.send_message(message.chat.id, responce)


def on_state(message):
    try:
        state = __try_vhost().State()
        responce = "State: %d (%s)" % (state, virt.STATE_NAME[state])
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.send_message(message.chat.id, responce)


def on_create(message):
    try:
        retcode = __try_vhost().Create()
        logging.debug(type(retcode))
        responce = "Start: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.send_message(message.chat.id, responce)


def on_destroy(message):
    try:
        retcode = __try_vhost().Destroy()
        logging.debug(type(retcode))
        responce = "Destroy: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.send_message(message.chat.id, responce)


def on_suspend(message):
    try:
        retcode = __try_vhost().Suspend()
        logging.debug(type(retcode))
        responce = "Suspend: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.send_message(message.chat.id, responce)


def on_resume(message):
    try:
        retcode = __try_vhost().Resume()
        logging.debug(type(retcode))
        responce = "Resume: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.send_message(message.chat.id, responce)


def on_shutdown(message):
    try:
        retcode = __try_vhost().ShutDown()
        logging.debug(type(retcode))
        responce = "Shutdown: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.send_message(message.chat.id, responce)


def on_reboot(message):
    try:
        retcode = __try_vhost().Reboot()
        logging.debug(type(retcode))
        responce = "Reboot: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.send_message(message.chat.id, responce)


def on_reset(message):
    try:
        retcode = __try_vhost().Reset()
        logging.debug(type(retcode))
        responce = "Reset: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.send_message(message.chat.id, responce)


def on_list(message):
    try:
        responce = "VList: %s" % ', '.join(map(str, virt.VConn.list()))
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.send_message(message.chat.id, responce)


def on_default(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Access denied")


HANDLERS = {
    # TODO: mk help from this
    # TODO: key: (func, max acl lvl, desc)
    "start": (on_start, 3, "Welcome message"),
    "help": (on_help, 3, "This page"),
    "active": (on_active, 3, "Check that is active"),
    "state": (on_state, 3, "Get state"),
    "suspend": (on_suspend, 2, "Suspend"),
    "resume": (on_resume, 2, "Resume after suspend"),
    "run": (on_create, 1, "Start (power up)"),
    "shutdown": (on_shutdown, 1, "Shut down (soft power off)"),
    "reboot": (on_reboot, 1, "Reboot (soft restart)"),
    "reset": (on_reset, 0, "Reset (hard restart)"),
    "kill": (on_destroy, 0, "Shut off (hard power off)"),
    "list": (on_list, 0, "List vhost IDs"),
}


def main():
    """Main procedure."""
    global data, bot, user_acl, cmd_acl, help_text
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
    # 3. setup ACL
    for _id, _acl in data.get('acl', dict()).items():
        user_acl[int(_id)] = _acl  # TODO: chk is_int, acl range
    # 4. setup tg-bot
    bot = telebot.TeleBot(data['bot']['token'], parse_mode=None)
    bot.add_custom_filter(CanUse())
    for k, v in HANDLERS.items():
        cmd_acl[k] = v[1]
        tip = "/%s: %s" % (k, v[2])
        for i in range(v[1]+1):
            help_text[i].append(tip)
        bot.register_message_handler(v[0], commands=[k], can_use=True)
    bot.register_message_handler(on_default)  # stub
    # print(help_text)
    # 4. go
    bot.infinity_polling()


if __name__ == '__main__':
    main()
