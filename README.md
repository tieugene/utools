# srvbot

Telegram-based server helper bot.

## Commands:

- vhost (`libvirt.virtDomain.`, protected by default, 1 vhost only):
  - [x] active (`isActive() -> bool`), pub
  - [x] state (`state()`), pub
  - [x] poweron (`create()`)
  - [x] suspend (`suspend()`), confidential
  - [x] resume (`resume()`)
  - [x] shutdown (`shutdown()`, soft)
  - [x] shutoff (`shutdownFlags(), destroy()`?)
  - [x] reboot (`reboot()`, soft)
  - [x] reset (`reset()`, hard)
- itself:
  - [ ] selfreboot (`init 6`, `systemctl reboot`)
  - […] _list vhosts [`--inactive`]


## Install

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
python3 -m venv srvbot
# or pyvenv --system-site-packages --symlinks srvbot
source srvbot/bin/activate
[pip install --upgrade pip]
pip install pyTelegramBotAPI
deactivate
```

## ToDo:
- […] state diagram
- [ ] systemd unit
- [ ] ACL
- [ ] decorate helper.virt.VHost mathods
- [ ] decorate srvbot.handle_X
- [ ] pre-action check (acts available; see below)
- [ ] i18n+l10n
- [ ] more logging
- [ ] list inactive vhosts
- [ ] *shortcuts (`vhost state <name>`)*

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

[^1]: Paused => Reboot == Reboot after Resume (delayed reboot)
[^2]: Paused => Reset == Reset after Resume (delayed reset)

## RTFM:

- https://avalon.land/blog/it/telegram-bot-on-centos7/
- https://max-ko.ru/60-sreda-razrabotki-venv-python3-v-centos-7.html

## misc

Symbols: &times; &cross; &check; &hellip;
