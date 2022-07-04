#!/usr/bin/env python3

# 1. std
import sys
import logging
# 2. 3rd
import telebot

# 3. local
from helper import pre, log, virt

# const
HELP = '''Commands available:
/help: this page
/vlist: vlist vhosts
/vstate: vhost status'''
# var
data: dict
bot: telebot.TeleBot
vconn: virt.VConn = None
vhost: virt.VHost = None


def try_vconn() -> virt.VConn:
    global vconn
    if not vconn:
        logging.debug("Try to create vconn")
        vconn = virt.VConn()
    return vconn


def try_vhost(name: str) -> virt.VHost:
    global vhost
    if not vhost:
        logging.debug("Try to create vhost")
        vhost = virt.VHost(try_vconn(), name)
    return vhost


def handle_help(message):
    bot.reply_to(message, HELP)


def handle_vlist(message):
    vids = try_vconn().vlist()
    bot.reply_to(message, str(vids))


def handle_vstate(message):
    state = try_vhost(data['vhost']).State()
    bot.reply_to(message, str(state))


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
    bot.register_message_handler(handle_help, commands=['help'])
    bot.register_message_handler(handle_vlist, commands=['vlist'])
    bot.register_message_handler(handle_vstate, commands=['vstate'])
    # 4. go
    bot.infinity_polling()


if __name__ == '__main__':
    main()
