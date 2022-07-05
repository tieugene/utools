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
python3 -m venv srvbot
# or pyvenv --system-site-packages --symlinks srvbot
source srvbot/bin/activate
[pip install --upgrade pip]
pip install pyTelegramBotAPI
deactivate
```

## ToDo:

### 0.0.2:

- [ ] [systemd unit](https://avalon.land/blog/it/telegram-bot-on-centos7/)
- [ ] ACL
- [ ] decorate helper.virt.VHost methods
- [ ] decorate srvbot.handle_X
- [ ] more logging
- [ ] list inactive vhosts
- […] state diagram

### 0.0.3:

- [ ] i18n+l10n
- [ ] pre-action check (acts available; see below)
- [ ] configurable command names

### x.y.z:

- [ ] multi-vhost
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
