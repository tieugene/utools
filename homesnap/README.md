# HomeSnap

Home backup snapshot

# Requirements

- python 3.6+
- rsync client
- external drive (optional)

## Install:

### Remote:

- install and setup `shofiled`
- install and setup `rsyncd` properly
- tune firewall

### Local:

1. install `homesnap` rpm
2. create `/etc/xdg/homesnap.json` or `/root/.config/homesnap.json` like sample below
3. `systemctl enable homesnap.timer; systemctl start homesnap.timer`

## Config sample

Sample config file with C-like comments:

```json5
{
  "mail": {
    "smtp": "smtp.yandex.com",  // default with smtp auth, port 465
    "mailfrom": "robot@mydomain.com",  // as 'from' as smtp login
    "mailpass": "smtpassword",  // smtp password
    "mailto": ["admin@mydomain.com", "boss@mydomain.com"]  // can be a string
  },
  "log": 5,  // syslog verbosity, optional
  "items": [  // list of source/dest (remote/local) pairs
    {
      "name": "ext",  // just id
      "opts": "-aqzAHX --del",  // rsync client additional options
      "schk": "http://172.16.1.1:8000",  // source tag (`showfiled` endpoint via VPN)
      "spath": "rsync://172.16.1.1/daily",  // source rsync endpoint to mirror (via VPN)
      "dchk": "/mnt/shares/backup/ext.txt",  // dest tag (local file) in pair to 'schk'
      "dpath": "/mnt/shares/backup/ext/daily",  // dest rsync endpoint in pair to 'spath'
      "epath": "/misc/extdrive/backup/ext"  // external drive folder
    }
  ]
}
```

## ToDo
- [ ] cfg dict workaroud (`d[key]` &rArr; `d.get(key)`)
