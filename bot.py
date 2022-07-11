#!/usr/bin/env python3
"""Telegram bot to handle KVM host."""
# 1. std
import enum
import sys
import logging
import functools
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
        user = message.from_user
        _uid = user.id
        _cmd = message.text
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
    bot.send_message(message.chat.id, WELCOME)


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
def on_active(_: telebot.types.Message):
    return "Active: " + ('✗', CHECK)[int(__try_vhost().isActive())]


@on_action
def on_state(_: telebot.types.Message):
    state = __try_vhost().State()
    return "State: %d (%s)" % (state, virt.STATE_NAME[state])


@on_action
def on_create(_: telebot.types.Message):
    retcode = __try_vhost().Create()  # 0 if ok
    return "Run: " + (str(retcode) if retcode else CHECK)


@on_action
def on_destroy(_: telebot.types.Message):
    retcode = __try_vhost().Destroy()
    return "Kill: " + (str(retcode) if retcode else CHECK)


@on_action
def on_suspend(_: telebot.types.Message):
    retcode = __try_vhost().Suspend()
    return "Suspend: " + (str(retcode) if retcode else CHECK)


@on_action
def on_resume(_: telebot.types.Message):
    retcode = __try_vhost().Resume()
    return "Resume: " + (str(retcode) if retcode else CHECK)


@on_action
def on_shutdown(_: telebot.types.Message):
    retcode = __try_vhost().ShutDown()
    return "Shutdown: " + (str(retcode) if retcode else CHECK)


@on_action
def on_reboot(_: telebot.types.Message):
    retcode = __try_vhost().Reboot()
    return "Reboot: " + (str(retcode) if retcode else CHECK)


@on_action
def on_reset(_: telebot.types.Message):
    retcode = __try_vhost().Reset()
    return "Reset: " + (str(retcode) if retcode else CHECK)


@on_action
def on_list(_: telebot.types.Message):
    return "VHosts: %s" % ', '.join(map(str, virt.VConn.list()))


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
        logging.warning("Access denied: %s by %d (%s)" % (message.text, user.id, user.full_name))
        bot.send_message(message.chat.id, "Access denied")


HANDLERS = {
    "start": (on_start, IEACLevel.User, "Welcome message"),
    "help": (on_help, IEACLevel.User, "This page"),
    "ask": (on_state, IEACLevel.User, "Get state"),
    "stop": (on_suspend, IEACLevel.User, "Suspend (pause)"),
    "resume": (on_resume, IEACLevel.Mgr, "Resume after suspend"),
    "run": (on_create, IEACLevel.Mgr, "Power on"),
    "shutdown": (on_shutdown, IEACLevel.Mgr, "Shut down (soft power off)"),
    "reboot": (on_reboot, IEACLevel.Mgr, "Reboot (soft restart)"),
    "reset": (on_reset, IEACLevel.Admin, "Reset (hard restart)"),
    "kill": (on_destroy, IEACLevel.Admin, "Shut off (hard power off)"),
    "active": (on_active, IEACLevel.Admin, "Check vhost is active"),
    "list": (on_list, IEACLevel.Admin, "List vhost IDs"),
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
        cmd_acl['/'+k] = v[1].value
        tip = "/%s: %s" % (k, v[2])
        for i in range(v[1].value + 1):
            help_text[i].append(tip)
        bot.register_message_handler(v[0], commands=[k], can_use=True)
    bot.register_message_handler(on_default)  # stub
    # 4. go
    bot.infinity_polling()


if __name__ == '__main__':
    main()
