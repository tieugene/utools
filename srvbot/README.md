# srvbot

Telegram-based KVM guest helper bot.

## Requirements

- python3 3.9+
- python3-libvirt (system)
- python3-aiogram (pip)

## Install

### rpm (not ready yet):
1. Install rpm
2. Create `/etc/xdg/srvbot.json` or `/root/.config/srvbot.json` like the sample below
3. `systemctl enable --now srvbot`

### Venv:

```bash
# CentOS9, F40 (root):
## 1. mk venv:
dnf install python3-libvirt
python3 -m venv --system-site-packages --symlinks /opt/pysandbox
source /opt/pysandbox/bin/activate
pip install aiogram
deactivate
## 2. copy sources:
mkdir /opt/pysandbox/srvbot
# cp srvbot.py srvbot.json locale/ => /opt/pysandbox/
# 3. test:
VIRTUAL_ENV=/opt/pysandbox /opt/pysandbox/bin/python3 /opt/pysandbox/srvbot/srvbot.py
# 4. productin:
cp srvbot.venv.service /usr/lib/systemd/system/srvbot.service
systemctl daemon-reload
systemctl enable --now srvbot.service
# check
journalctl -f -u srvbot.service
```

## State/Action

| st | State\Act | crt | dst | sus | rsm | shtdn | rbt   | rst   |
|----|-----------|-----|-----|-----|-----|-------|-------|-------|
| 1  | Running   | ×   | 5   | 3   | ×   | 5     | 1     | 1     |
| 2  | Blocked   | …   |     |     |     |       |       |       |
| 3  | Paused    | ×   | 5   | 3   | 1   | ×     | 3[^1] | 3[^2] |
| 4  | ShutDown  | …   |     |     |     |       |       |       |
| 5  | ShutOff   | 1   | ×   | ×   | ×   | ×     | ×     | ×     |
| 6  | Crashed   | …   |     |     |     |       |       |       |
| 7  | PBSuspend |     |     |     |     |       |       |       |

*ToDo: Paused <> PausedReboot <> PausedReset <> Destroy*

[^1]: Paused => Reboot == Reboot after Resume (delayed reboot)
[^2]: Paused => Reset == Reset after Resume (delayed reset)

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
  "acl": [  // access control list
    {  // 'cmd' commands are available for 'uid' Tg users
      "cmd": ["state", "suspend", "resume", "create", "reboot", "shutdown", "reset", "destroy", "active"],
      "uid": [123456789]  // like admin
    },
    {
      "cmd": [
        "state",
        "suspend",
        "resume"
      ],
      "uid": [
        987654322,
        192837465
      ]
      // ordinar users
    }
  ]
}
```

### BotFather:

 - [x] /setjoingroups: Disable
 - [x] /setprivacy: Enable
 - [ ] /setcommands: 
