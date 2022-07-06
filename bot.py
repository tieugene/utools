#!/usr/bin/env python3
"""Telegram bot to handle KVM host.
:todo: handle_x into decorator
"""
# 1. std
import enum
import sys
import logging
# 2. 3rd
# noinspection PyPackageRequirements
from typing import Optional

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
        """
        Conditions:
        - txt must be cmd (/...)
        - cmd must be known (in cmd's ACL)
        - user must be known (in user's ACL)
        - user.ACL must be <= cmd.ACL
        :param message:
        :return: True if access ok
        """
        logging.debug("can_use: uid=%d, cmd=%s" % (message.from_user.id, message.text))
        u_acl = _get_user_acl(message)
        c_acl = _get_cmd_acl(message)
        if u_acl is not None and c_acl is not None:
            logging.debug("u_acl=%d, c_acl=%d" % (u_acl, c_acl))
            return u_acl <= c_acl
        return False


def __try_vhost() -> virt.VHost:
    global vhost
    if not vhost:
        logging.debug("Try to create vhost")
        vhost = virt.VHost(data['vhost'])
    return vhost


def _get_user_acl(message: telebot.types.Message) -> Optional[int]:
    return user_acl.get(message.from_user.id)


def _get_cmd_acl(message: telebot.types.Message) -> Optional[int]:
    return cmd_acl.get(message.text)


def on_start(message: telebot.types.Message):
    bot.send_message(message.chat.id, WELCOME)


def on_help(message: telebot.types.Message):
    bot.send_message(message.chat.id, '\n'.join(help_text[user_acl[message.from_user.id]]))


def on_active(message: telebot.types.Message):
    try:
        response = "Active: " + ('✗', CHECK)[int(__try_vhost().isActive())]
    except virt.YAPBKVMErrorError as e:
        response = str(e)
        logging.error(response)
    bot.send_message(message.chat.id, response)


def on_state(message: telebot.types.Message):
    try:
        state = __try_vhost().State()
        response = "State: %d (%s)" % (state, virt.STATE_NAME[state])
    except virt.YAPBKVMErrorError as e:
        response = str(e)
        logging.error(response)
    bot.send_message(message.chat.id, response)


def on_create(message: telebot.types.Message):
    try:
        retcode = __try_vhost().Create()  # 0 if ok
        response = "Start: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        response = str(e)
        logging.error(response)
    bot.send_message(message.chat.id, response)


def on_destroy(message: telebot.types.Message):
    try:
        retcode = __try_vhost().Destroy()
        response = "Destroy: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        response = str(e)
        logging.error(response)
    bot.send_message(message.chat.id, response)


def on_suspend(message: telebot.types.Message):
    try:
        retcode = __try_vhost().Suspend()
        response = "Suspend: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        response = str(e)
        logging.error(response)
    bot.send_message(message.chat.id, response)


def on_resume(message: telebot.types.Message):
    try:
        retcode = __try_vhost().Resume()
        response = "Resume: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        response = str(e)
        logging.error(response)
    bot.send_message(message.chat.id, response)


def on_shutdown(message: telebot.types.Message):
    try:
        retcode = __try_vhost().ShutDown()
        response = "Shutdown: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        response = str(e)
        logging.error(response)
    bot.send_message(message.chat.id, response)


def on_reboot(message: telebot.types.Message):
    try:
        retcode = __try_vhost().Reboot()
        response = "Reboot: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        response = str(e)
        logging.error(response)
    bot.send_message(message.chat.id, response)


def on_reset(message: telebot.types.Message):
    try:
        retcode = __try_vhost().Reset()
        response = "Reset: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        response = str(e)
        logging.error(response)
    bot.send_message(message.chat.id, response)


def on_list(message: telebot.types.Message):
    try:
        response = "VList: %s" % ', '.join(map(str, virt.VConn.list()))
    except virt.YAPBKVMErrorError as e:
        response = str(e)
        logging.error(response)
    bot.send_message(message.chat.id, response)


def on_default(message: telebot.types.Message):
    """Stub for unknow user, unknown command, access denied"""
    user = message.from_user
    if user.id not in user_acl:
        logging.warning("Unknown user: %d - %s (username=%s, first_name=%s, last_name=%s)" % (
            user.id,
            user.full_name,
            user.username,
            user.first_name,
            user.last_name
        ))
        bot.send_message(message.chat.id, "Брысь!")
    elif message.text not in cmd_acl:
        bot.send_message(message.chat.id, "Unknown command")
    else:
        bot.send_message(message.chat.id, "Access denied")


HANDLERS = {
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
    if 'log' in data:
        log.setLogger(data['log'])
    if 'tglog' in data:
        # logger = telebot.logger
        telebot.logger.setLevel(log.LOG_LEVEL[data['tglog']])
    # 3. setup ACL
    for _id, _acl in data.get('acl', dict()).items():
        user_acl[int(_id)] = _acl  # TODO: chk is_int, acl range
    # 4. setup tg-bot
    bot = telebot.TeleBot(data['bot']['token'], parse_mode=None)
    bot.add_custom_filter(CanUse())
    for k, v in HANDLERS.items():
        cmd_acl['/'+k] = v[1]
        tip = "/%s: %s" % (k, v[2])
        for i in range(v[1]+1):
            help_text[i].append(tip)
        bot.register_message_handler(v[0], commands=[k], can_use=True)
    bot.register_message_handler(on_default)  # stub
    # 4. go
    bot.infinity_polling()


if __name__ == '__main__':
    main()
