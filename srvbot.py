#!/usr/bin/env python3
"""Telegram bot to handle KVM host.
:todo: handle_x into decorator
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
/help: this page
/list: list vhosts
/active: whether vhost is running
/state: vhost status
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
        responce = "VList: %s" % ', '.join(map(str, virt.VConn.vlist()))
    except exc.YAPBKVMErrorError as e:
        responce = "Err: " + str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def handle_active(message):
    try:
        responce = "Active: " + ("-", "+")[int(__try_vhost().isActive())]
    except exc.YAPBKVMErrorError as e:
        responce = "Err: " + str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


def handle_state(message):
    try:
        state = __try_vhost().State()
        responce = "State: %d (%s)" % (state, virt.STATE_NAME[state])
    except exc.YAPBKVMErrorError as e:
        responce = "Err: " + str(e)
        logging.error(responce)
    bot.reply_to(message, responce)


HANDLERS = {
    "help": handle_help,
    "list": handle_list,
    "active": handle_active,
    "state": handle_state,
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
        bot.register_message_handler(v, commands=[k] if isinstance(k, str) else k)
    # 4. go
    bot.infinity_polling()


if __name__ == '__main__':
    main()
