# HomeSnap

Home backupnSnapshot

# Requirements
- python 3.6+
- python3-libvirt 4.5.0+

# Advantages
- [x] json config
- [ ] per-vhost config
- [ ] backing up:
  - [ ] KVM ntfs volume
  - [ ] LXC folders
  - [x] rsync local dir-to-dir
  - [ ] pack (7za, tar)
- [ ] copying:
  - [x] rsync local drive-to-drive
  - [x] rsync local dir to remote
  - [ ] ftp
  - [ ] rclone?
- [ ] rotates (day/week/month)
- [x] email
- [x] log

## Modules:
- [x] cli/cfg
- [ ] vhost: ctl KVM vhosts - state/freeze/resume(host) (class?); libvirt
- [ ] vdrive: ctl vdrives (maybe from kvm?): mount/umount (class?); CLI
- [x] mail: smtp client
- [x] rsync: rsync frontend; CLI
- [ ] pack: 7za/tar frontend; CLI
- [x] log

## TODO
### Teach:
- python-libvirt
- PyCharm remote debug
- guest-agent
- JSON Schema

## host025:
- copy `host025.py` into somewhere
- mk `host025.json` there or in `/etc/`
- systemctl:
   ```bash
   cp {host025.service,homesnap.timer} /etc/systemd/system/
   systemctl daemon-reload
   systemctl enable host025.service
   [systemctl start host025.serice]
   systemctl enable homesnap.timer
   systemctl start homesnap.timer
   ```

## ToDo
- [ ] cfg dict workaroud (`d[key]` &rArr; `d.get(key)`)
- [ ] `sample/`
- [ ] ~~logrotate~~
- [ ] spec
- [ ] `setup.py` (bin + lib)
- [ ] use `ulib`
