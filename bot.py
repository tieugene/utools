#!/usr/bin/env python3
"""Telegram bot to handle KVM host."""
# 1. std
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
data: dict              # loaded config
bot: telebot.TeleBot    # bot itself
vhost: virt.VHost       # the vhost what control to
alias2cmd: dict         # alias:str -> cmd:str
users: set = set()      # registered users (set[int])
cmd_acl: dict = {}      # cmd:str -> users:set
help_text: dict = {}    # cmd -> help string
# TODO: cmd enum


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
            _uid: int = user.id
            _cmd: str = message.text[1:]
            _cmd = alias2cmd.get(_cmd, _cmd)  # use original cmd anyway
            logging.debug("can_use: uid=%d, cmd=%s" % (_uid, _cmd))
            if _uid in users and _uid in cmd_acl.get(_cmd, {}):
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
    # TODO: cache it
    uid = message.from_user.id
    help_list = []
    for cmd, uids in cmd_acl.items():
        if uid in uids and cmd in help_text:
            logging.debug(f"Help for {uid} available: {cmd}")
            help_list.append(help_text[cmd])
        else:
            logging.debug(f"Help for {uid} disabled: {cmd}")
    bot.send_message(message.chat.id, '\n'.join(help_list))


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
    logging.debug(f"Default stub: user={user.id}, cmd='{message.text}'")
    if user.id not in users:
        logging.warning("Unknown user: %d - %s (username=%s, first_name=%s, last_name=%s)" % (
            user.id,
            user.full_name,
            user.username,
            user.first_name,
            user.last_name
        ))
        bot.send_message(message.chat.id, _("Scat!"))
    else:
        if not message.text.startswith('/'):
            bot.send_message(message.chat.id, _("Not a command."))
        else:
            cmd = message.text[1:]
            if cmd not in cmd_acl:
                bot.send_message(message.chat.id, _("Unknown command."))
            else:
                bot.send_message(message.chat.id, _("Access denied"))
                logging.warning("Access denied: %s by %d (%s)" % (message.text, user.id, user.full_name))


HANDLERS = {  # cmd => (handler, help)
    "start": (on_start, None),
    "help": (on_help, _("This page")),
    "state": (on_state, _("State")),
    "suspend": (on_suspend, _("Suspend")),
    "resume": (on_resume, _("Resume (after suspend)")),
    "create": (on_create, _("Power on")),
    "reboot": (on_reboot, _("Reboot")),
    "shutdown": (on_shutdown, _("Power off")),
    "reset": (on_reset, _("Reset (force reboot)")),
    "destroy": (on_destroy, _("Power off (force)")),
    "active": (on_active, _("Check is active")),
    "list": (on_list, _("List vhost IDs")),
}


def main():
    """Main procedure."""
    global data, vhost, bot, cmd_acl, alias2cmd, users, help_text  # , user_acl
    # 1. load cfg
    vhost = None
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
    # 3. setup aliases, ACL
    alias2cmd = data.get('alias', dict())
    __cmd2alias: dict = dict(map(reversed, alias2cmd.items()))
    cmd_acl = dict([(c, set()) for c in HANDLERS.keys()])
    for acl in data.get('acl', []):
        uids = set(acl['uid'])  # users for current ACL cmd set
        users.update(uids)      # expand global users list
        for cmd in acl['cmd']:  # create/update ACL
            if cmd not in HANDLERS:
                sys.exit(f"Unknown command in cfg: {cmd}")
            cmd_acl[cmd].update(uids)
    # default ACL items
    cmd_acl['start'] = cmd_acl['help'] = users
    # 4. setup tg-bot
    bot = telebot.TeleBot(data['token'], parse_mode=None)
    bot.add_custom_filter(CanUse())
    for cmd, v in HANDLERS.items():
        cmd_list = [cmd]          # for help and trigger
        if cmd in __cmd2alias:
            cmd_list.append(__cmd2alias[cmd])
        bot.register_message_handler(v[0], commands=cmd_list, can_use=True)
        if v[1]:
            help_text[cmd] = "%s: %s" % (', '.join([f"/{s}" for s in cmd_list]), v[1])
    bot.register_message_handler(on_default)  # stub
    # 4. go
    bot.infinity_polling()


if __name__ == '__main__':
    main()
