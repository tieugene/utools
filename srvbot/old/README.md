# srvbot

Telegram-based server helper bot.

## Requirements

- python3 3.6+
- python3-pyTelegramBotAPI
- python3-libvirt
- python3-ulib

## Install

1. Install rpm
2. Create `/etc/xdg/srvbot.json` or `/root/.config/srvbot.json` like the sample below
3. `systemctl enable --now srvbot`

### Venv

Usage in old CentOS' requires special
[actions](https://max-ko.ru/60-sreda-razrabotki-venv-python3-v-centos-7.html):

```bash
# CentOS7:
# yum install python36-virtualenv python36-libvirt
# CentOS8:
dnf install python3-virtualenv python3-libvirt
cd /opt
python3 -m venv pysandbox
# or pyvenv --system-site-packages --symlinks pysandbox
source pysandbox/bin/activate
pip install --upgrade pip
pip install pyTelegramBotAPI
deactivate
```

## State/Action

st | State\Act| crt | dst | sus | rsm |shtdn| rbt | rst 
---|----------|-----|-----|-----|-----|-----|-----|-----
 1 | Running  |  ×  |  5  |  3  |  ×  |  5  |  1  |  1
 2 | Blocked  |  …  |     |     |     |     |     |  
 3 | Paused   |  ×  |  5  |  3  |  1  |  ×  |3[^1]|3[^2]
 4 | ShutDown |  …  |     |     |     |     |     |  
 5 | ShutOff  |  1  |  ×  |  ×  |  ×  |  ×  |  ×  |  ×
 6 | Crashed  |  …  |     |     |     |     |     |  
 7 | PBSuspend|     |     |     |     |     |     |  

*ToDo: Paused <> PausedReboot <> PausedReset <> Destroy*

[^1]: Paused => Reboot == Reboot after Resume (delayed reboot)
[^2]: Paused => Reset == Reset after Resume (delayed reset)

### Actions

- State
- Suspend
- Resume
- Shutdwn
- Create
- Reboot
- Reset
- Destroy
- Active
- List

## i18n

1. Prepare i18n: `xgettext -o locale/srvbot.pot bot.py`
2. Mk l10n: `cp locale/srvbot.pot locale/ru/LC_MESSAGES/srvbot.po`
3. Translate (`poedit`)
4. Update l10n: `msgmerge -U locale/ru/LC_MESSAGES/srvbot.po locale/srvbot.pot`
5. Compile: `msgfmt -o locale/ru/LC_MESSAGES/srvbot.mo locale/ru/LC_MESSAGES/srvbot.po`

## Sample

Sample config file (json with C-style comments):

```json5
{
  "log": 5,  //  log level (optional, default - no)
  "tglog": 3,  // Telegram log level (optional, default - no)
  "token": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",  // mandatory
  "vhost": "w10",  // name of KVM guest, mandatory
  "alias": {  // command aliases, optional
    "стоп": "suspend",
    "старт": "resume"
  },
  "acl": [  // access control list
    {  // 'cmd' commands are available for 'uid' Tg users
      "cmd": ["state", "suspend", "resume", "create", "reboot", "shutdown", "reset", "destroy", "active"],
      "uid": [123456789]  // like admin
    },
    {
      "cmd": ["state", "suspend", "resume"],
      "uid": [987654322, 192837465]  // ordinar users
  ]
}
```

## ToDo:

### 0.0.4:

Aim: expanding

- [ ] pre-action check (acts available; see below)
- [ ] list inactive vhosts
- [ ] multi-vhost
- [ ] *shortcuts (`vhost state <name>`)*

### BotFather:

 - [x] /setjoingroups: Disable
 - [x] /setprivacy: Enable
 - [ ] /setcommands: 
