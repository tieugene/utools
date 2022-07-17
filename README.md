# srvbot

Telegram-based server helper bot.

## Requirements

- python 3.6+
- python-pyTelegramBotAPI
- python-libvirt

## Install

[RTFM](https://max-ko.ru/60-sreda-razrabotki-venv-python3-v-centos-7.html)

### CentOS 7
```bash
yum install python36-virtualenv python36-libvirt
```

### CentOS 8
```bash
dnf install python3-virtualenv python3-libvirt
```

### CentOS all
```bash
cd /opt
python3 -m venv pysandbox
# or pyvenv --system-site-packages --symlinks pysandbox
source pysandbox/bin/activate
[pip install --upgrade pip]
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

- Active
- State
- Suspend
- Resume
- Create
- Shutdwn
- Reboot
- Reset
- Destroy
- List

## ToDo:

### x.y.z:

Aim: expanding

- [ ] pre-action check (acts available; see below)
- [ ] list inactive vhosts
- [ ] multi-vhost
- [ ] *shortcuts (`vhost state <name>`)*

### BotFather:

 - [x] /setjoingroups: Disable
 - [x] /setprivacy: Enable
 - [ ] /setcommands: 

## Done

### 0.0.2:

Aim: make usable

- [x] [systemd unit](https://avalon.land/blog/it/telegram-bot-on-centos7/)
- [x] ACL
- [x] decorate srvbot.handle_X
- [x] decorate helper.virt.VHost methods
- [x] state diagram
- [x] more logging

### 0.0.3:

Aim: extending

- [x] configurable command aliases
- [x] configurable ACL
- [x] i18n+l10n

## i18n

1. Prepare i18n: `xgettext -o locale/srvbot.pot bot.py`
2. Mk l10n: `cp locale/srvbot.pot locale/ru/LC_MESSAGES/srvbot.po`
3. Translate (`poedit`)
4. Update l10n: `msgmerge -U locale/ru/LC_MESSAGES/srvbot.po locale/srvbot.pot`
5. Compile: `msgfmt -o locale/ru/LC_MESSAGES/srvbot.mo locale/ru/LC_MESSAGES/srvbot.po`
