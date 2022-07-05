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
from helper import pre, log, virt, exc

# const
HELP = '''Commands available:
/help, /?: this page
/list: List vhosts
/active: Check whether vhost is running
/state: Get vhost status
/start: Run vhost
/suspend: Suspend vhost
/resume: Resume vhost
'''
# var
data: dict
bot: telebot.TeleBot
vhost: virt.VHost = None


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
    except exc.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def handle_active(message):
    try:
        responce = "Active: " + ("-", "+")[int(__try_vhost().isActive())]
    except exc.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def handle_state(message):
    try:
        state = __try_vhost().State()
        responce = "State: %d (%s)" % (state, virt.STATE_NAME[state])
    except exc.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def handle_create(message):
    try:
        retcode = __try_vhost().Create()
        logging.debug(type(retcode))
        responce = "Started: " + str(retcode)
    except exc.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def handle_suspend(message):
    try:
        retcode = __try_vhost().Suspend()
        logging.debug(type(retcode))
        responce = "Suspended: " + str(retcode)
    except exc.YAPBKVMErrorError as e:
        responce = str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def handle_resume(message):
    try:
        retcode = __try_vhost().Resume()
        logging.debug(type(retcode))
        responce = "Resumed: " + str(retcode)
    except exc.YAPBKVMErrorError as e:
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
