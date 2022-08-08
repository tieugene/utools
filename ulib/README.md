# &mu;-lib

Utility micro-library

## Requirements

- python 3.6+
- python3-appdirs
- python3-libvirt 4.5.0+

## Modules

- [`backup`](ulib/backup.py) - *(stub)*
- [`exc`](ulib/exc.py) - exceptions base
- [`log`](ulib/log.py) - logging
- [`mail`](ulib/mail.py) - smtp client
- [`pre`](ulib/pre.py) - prepend tasks (config, CLI)
- [`rsync`](ulib/rsync.py) - `rsync` (CLI) wrapper
- [`stamp`](ulib/stamp.py) - handle stamp file
- [`vdrive`](ulib/vdrive.py) - *(stub)* ctl vdrives (maybe from kvm?): mount/umount (class?); CLI
- [`virt`](ulib/virt.py) - libvirt wrapper
- `pack` - `7za`/`tar` (CLI) wrapper

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

## TODO

- split by subpackages
