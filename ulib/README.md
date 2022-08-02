# &mu;-lib

Utility micro-library

## Requirements

- python 3.6+
- python3-libvirt 4.5.0+

## TOC

- `exc.py` - exceptions base
- `log.py` - logging
- `pre.py` - prepend tasks (config, CLI)
- `virt.py` - libvirt wrapper

## Advantages
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
