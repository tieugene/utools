#!/usr/bin/env python3
"""Telegram bot to handle KVM host."""
# 1. std
import enum
import os
import sys
import logging
import functools
import gettext
# 2. 3rd
# noinspection PyPackageRequirements
import telebot
# 3. local
from helper import pre, log, virt
# i18n
localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')  # TODO: or appdirs.site_data_dir()
translate = gettext.translation('srvbot', localedir=localedir)
_ = translate.gettext
# const
ACL_LEVELS = 4  # 0..3
CHECK = '✓'
STATE_NAME = (
    _("No state"),
    _("Running"),
    _("Blocked"),
    _("Paused"),
    _("Shutdown"),
    _("Shutoff"),
    _("Crashed"),
    _("PM Suspended")
)
# var
data: dict  # loaded config
bot: telebot.TeleBot  # bot itself
vhost: virt.VHost = None  # the vhost what control to
user_acl: dict = {}     # user.id -> ACL level
cmd_acl: dict = {}      # cmd -> ACL level
alias2cmd: dict         # alias -> cmd
help_text: list = [[], [], [], []]  # separate for each ACL level


class IEACLevel(enum.IntEnum):
    Admin = 0
    Mgr = 1
    User = 2


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
        if message.text.startswith('/'):  # commands only
            user = message.from_user
            _uid = user.id
            _cmd = message.text[1:]
            _cmd = alias2cmd.get(_cmd, _cmd)  # use original cmd anyway
            logging.debug("can_use: uid=%d, cmd=%s" % (_uid, _cmd))
            u_acl = user_acl.get(_uid)
            c_acl = cmd_acl.get(_cmd)
            if u_acl is not None and c_acl is not None and u_acl <= c_acl:
                logging.info("Call %s by %d (%s)" % (_cmd, _uid, user.full_name))
                return True
        return False


def __try_vhost() -> virt.VHost:
    global vhost
    if not vhost:
        logging.debug("Try to create vhost")
        vhost = virt.VHost(data['vhost'])
    return vhost


def on_start(message: telebot.types.Message):
    bot.send_message(message.chat.id, _("Welcome.\nSend '/help' for list commands available."))


def on_help(message: telebot.types.Message):
    bot.send_message(message.chat.id, '\n'.join(help_text[user_acl[message.from_user.id]]))


def on_action(func: callable):
    @functools.wraps(func)
    def wrapper(message: telebot.types.Message):
        try:
            response = func(message)
        except virt.YAPBKVMErrorError as e:
            response = str(e)
            logging.error(response)
        bot.send_message(message.chat.id, response)
    return wrapper


@on_action
def on_active(__: telebot.types.Message) -> str:
    return _("Active") + ': ' + ('✗', CHECK)[int(__try_vhost().isActive())]


@on_action
def on_state(__: telebot.types.Message) -> str:
    state = __try_vhost().State()
    return _("State") + ": %d (%s)" % (state, STATE_NAME[state])


@on_action
def on_create(__: telebot.types.Message) -> str:
    retcode = __try_vhost().Create()  # 0 if ok
    return _("Power on") + ': ' + (str(retcode) if retcode else CHECK)


@on_action
def on_destroy(__: telebot.types.Message) -> str:
    retcode = __try_vhost().Destroy()
    return _("Power off (force)") + ': ' + (str(retcode) if retcode else CHECK)


@on_action
def on_suspend(__: telebot.types.Message) -> str:
    retcode = __try_vhost().Suspend()
    return _("Suspend") + ': ' + (str(retcode) if retcode else CHECK)


@on_action
def on_resume(__: telebot.types.Message) -> str:
    retcode = __try_vhost().Resume()
    return _("Resume") + ': ' + (str(retcode) if retcode else CHECK)


@on_action
def on_shutdown(__: telebot.types.Message) -> str:
    retcode = __try_vhost().ShutDown()
    return _("Power off") + ': ' + (str(retcode) if retcode else CHECK)


@on_action
def on_reboot(__: telebot.types.Message) -> str:
    retcode = __try_vhost().Reboot()
    return _("Reboot") + ': ' + (str(retcode) if retcode else CHECK)


@on_action
def on_reset(__: telebot.types.Message) -> str:
    retcode = __try_vhost().Reset()
    return _("Reset") + ': ' + (str(retcode) if retcode else CHECK)


@on_action
def on_list(__: telebot.types.Message):
    return "VHosts: %s" % ', '.join(map(str, virt.VConn.list()))


def on_default(message: telebot.types.Message):
    """Stub for unknown user, unknown command, access denied"""
    user = message.from_user
    if user.id not in user_acl:
        logging.warning("Unknown user: %d - %s (username=%s, first_name=%s, last_name=%s)" % (
            user.id,
            user.full_name,
            user.username,
            user.first_name,
            user.last_name
        ))
        bot.send_message(message.chat.id, _("Scat!"))
    elif message.text not in cmd_acl:
        bot.send_message(message.chat.id, _("Unknown command."))
    else:
        logging.warning("Access denied: %s by %d (%s)" % (message.text, user.id, user.full_name))
        bot.send_message(message.chat.id, _("Access denied"))


HANDLERS = {
    "start": (on_start, IEACLevel.User, _("Welcome message")),
    "help": (on_help, IEACLevel.User, _("This page")),
    "state": (on_state, IEACLevel.User, _("State")),
    "suspend": (on_suspend, IEACLevel.User, _("Suspend")),
    "resume": (on_resume, IEACLevel.Mgr, _("Resume (after suspend)")),
    "create": (on_create, IEACLevel.Mgr, _("Power on")),
    "reboot": (on_reboot, IEACLevel.Mgr, _("Reboot")),
    "shutdown": (on_shutdown, IEACLevel.Mgr, _("Power off")),
    "reset": (on_reset, IEACLevel.Admin, _("Reset (force reboot)")),
    "destroy": (on_destroy, IEACLevel.Admin, _("Power off (force)")),
    "active": (on_active, IEACLevel.Admin, _("Check is active")),
    "list": (on_list, IEACLevel.Admin, _("List vhost IDs")),
}


def main():
    """Main procedure."""
    global data, bot, user_acl, cmd_acl, alias2cmd, help_text
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
    # 3. setup ACL, aliases
    for _id, _acl in data.get('acl', dict()).items():
        user_acl[int(_id)] = _acl
    alias2cmd = data.get('alias', dict())
    cmd2alias: dict = dict(map(reversed, alias2cmd.items()))
    # 4. setup tg-bot
    bot = telebot.TeleBot(data['token'], parse_mode=None)
    bot.add_custom_filter(CanUse())
    for cmd, v in HANDLERS.items():
        func, lvl, desc = v
        cmd_acl[cmd] = lvl.value  # set command ACL (cmd => min user lvl)
        cmd_list = [cmd]          # for help and trigger
        if cmd in cmd2alias:
            cmd_list.append(cmd2alias[cmd])
        tip = "%s: %s" % (', '.join([f"/{s}" for s in cmd_list]), desc)  # cmd help string
        for i in range(lvl.value + 1):
            help_text[i].append(tip)  # construct helps for each ACL level
        bot.register_message_handler(func, commands=cmd_list, can_use=True)
    bot.register_message_handler(on_default)  # stub
    # 4. go
    bot.infinity_polling()


if __name__ == '__main__':
    main()
