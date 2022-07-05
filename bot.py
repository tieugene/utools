#!/usr/bin/env python3
"""Telegram bot to handle KVM host.
:todo: handle_x into decorator
:todo: auth
"""
# 1. std
import sys
import logging
# 2. 3rd
import telebot
# 3. local
from helper import pre, log, virt

# const
HELP = '''= Commands available: =
/help, /?: this page
/list: List vhosts
- Vhost control: -
/active: Check whether is running
/state: Get status
/start: Run
/suspend: Suspend
/resume: Resume after suspend
/reboot: Reboot (soft)
/reset: Reset (hard)
/shutdown: Shutdown (soft)
/poweroff: Power Off (hard)
'''
CHECK = '✓'
# var
data: dict
bot: telebot.TeleBot
vhost: virt.VHost = None

# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)


def __try_vhost() -> virt.VHost:
    global vhost
    if not vhost:
        logging.debug("Try to create vhost")
        vhost = virt.VHost(data['vhost'])
    return vhost


def handle_help(message):
    bot.reply_to(message, HELP)


def handle_list(message):
    try:
        responce = "VList: %s" % ', '.join(map(str, virt.VConn.list()))
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def handle_active(message):
    try:
        responce = "Active: " + ('✗', CHECK)[int(__try_vhost().isActive())]
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def handle_state(message):
    try:
        state = __try_vhost().State()
        responce = "State: %d (%s)" % (state, virt.STATE_NAME[state])
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def handle_create(message):
    try:
        retcode = __try_vhost().Create()
        logging.debug(type(retcode))
        responce = "Start: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def handle_destroy(message):
    try:
        retcode = __try_vhost().Destroy()
        logging.debug(type(retcode))
        responce = "Destroy: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def handle_suspend(message):
    try:
        retcode = __try_vhost().Suspend()
        logging.debug(type(retcode))
        responce = "Suspend: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def handle_resume(message):
    try:
        retcode = __try_vhost().Resume()
        logging.debug(type(retcode))
        responce = "Resume: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def handle_shutdown(message):
    try:
        retcode = __try_vhost().ShutDown()
        logging.debug(type(retcode))
        responce = "Shutdown: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def handle_reboot(message):
    try:
        retcode = __try_vhost().Reboot()
        logging.debug(type(retcode))
        responce = "Reboot: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def handle_reset(message):
    try:
        retcode = __try_vhost().Reset()
        logging.debug(type(retcode))
        responce = "Reset: " + (str(retcode) if retcode else CHECK)
    except virt.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


HANDLERS = {  # TODO: mk help from this
    ("help", '?'): handle_help,
    "list": handle_list,
    "active": handle_active,
    "state": handle_state,
    "start": handle_create,
    "suspend": handle_suspend,
    "resume": handle_resume,
    "reboot": handle_reboot,
    "reset": handle_reset,
    "shutdown": handle_shutdown,
    "poweroff": handle_destroy,
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
    # 3. setup tg-bot
    bot = telebot.TeleBot(data['bot']['token'], parse_mode=None)
    for k, v in HANDLERS.items():
        bot.register_message_handler(v, commands=[k] if isinstance(k, str) else list(k))
    # 4. go
    bot.infinity_polling()


if __name__ == '__main__':
    main()
