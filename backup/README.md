# backup

## Requires:
- dump
- rsync
- virsh
- fuse[3] (mount/umount)
- arc[hivers] (7zip, tar)
- comp[ressors] (zstd/pigz/pbzip2)
- smtp client

## Objects:
- self (dump)
- dox (rsync)
- 1c7 (arc)
- 1c8 (arc|comp)
- kvm virt hosts (?)
- kvm virt disks (comp)
- lxc virt hosts
- lxc virt disks (arc)

## Storages:
- local disk (rsync)
- hetzner storage (ftp/ftps/sftp/scp/smp/cifs/borgbackup/rsync@ssh/https/webdav)
- ya.disk (webdav)

## misc
- web-frontend
- restore

## RTFM
- https://blog.finxter.com/how-to-call-an-external-command-in-python/
- https://pypi.org/project/BackuPy/

## Teach
- borg
- ~~libguestfs-rsync~~ - mount remote rsyncd
- ~~libguestfs-python~~ - explore image by python
- virt-tar-out (libguestfs-tools-c)

## Notes
- mk 'current' -> daily/... symlink
- email just "OK" or "Error"+log
