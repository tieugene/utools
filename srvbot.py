#!/usr/bin/env python3

# 1. std
import sys
# 2. 3rd
import telebot
# 3. local
from helper import pre, log, virt
# const
HELP = '''Commands available:
/help: this page
/vlist: list vhosts'''
# var
bot: telebot.TeleBot
vconn: virt.VConn
vdom: virt.VHost


def handle_help(message):
    bot.reply_to(message, HELP)


def handle_vlist(message):
    global vconn
    vconn = virt.VConn()
    vids = vconn.list()
    bot.reply_to(message, str(vids))


def main():
    """Main procedure."""
    global bot
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
    # 4. go
    bot.infinity_polling()


if __name__ == '__main__':
    main()
