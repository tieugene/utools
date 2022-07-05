# srvbot

Telegram-based server helper bot

## Commands:
- vhost (`libvirt.virtDomain.`, protected by default):
  - [x] active (`isActive() -> bool`), pub
  - [x] state (`state()`), pub
  - [x] poweron (`create()`)
  - [x] suspend (`suspend()`), confidential
  - [x] resume (`resume()`)
  - [ ] shutdown (`shutdown()`, soft)
  - [ ] shutoff (`shutdownFlags(), destroy()`?)
  - [ ] reboot (`reboot()`, soft)
  - [ ] reset (`reset()`, hard)
- itself:
  - [ ] selfreboot (`init 6`, `systemctl reboot`)

## Features:
- [ ] user ACL (cfg), TODO
- [x] single vhost only
- [ ] _shortcuts (`vhost status <name>`)_
- [x] _list vhosts [`--inactive`] (`libvirt.virtConnect().listDomainsID()`)_

## Notes:
- CentOS 7: python 3.6.8, ~~pytelegrambotapi~~ (3.7.6: ...): https://koji.fedoraproject.org/koji/taskinfo?taskID=89087861
- CentOS 8: python 3.6.8 (3.9.x), pytelegrambotapi 3.7.6 (4.6.0: wait): https://koji.fedoraproject.org/koji/taskinfo?taskID=89088017

## RTFM:
- https://avalon.land/blog/it/telegram-bot-on-centos7/
- https://max-ko.ru/60-sreda-razrabotki-venv-python3-v-centos-7.html

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
- [ ] auth
- [ ] decorate virt.VHost mathods
- [ ] decorate handle_X
- [ ] state diagram
