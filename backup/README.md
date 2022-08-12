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

## Limitations
- run as root (due libvirt)
- KVM guests only (yet)
- rsync 1-level folders

## RTFM

- [kpartx+mount](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/5/html/virtualization/sect-virtualization-troubleshooting_xen-accessing_data_on_guest_disk_image)
- [qemu-nbd+mount](https://gist.github.com/shamil/62935d9b456a6f9877b5)
- [kpartx+pysh](https://gist.github.com/sandeep-datta/7375280)
- [libguestfs-tools:guest[u]mount](https://linuxconfig.org/access-and-modify-virtual-machines-disk-images-with-libguestfs-tools)
- [python3-libguestfs](https://libguestfs.org/guestfs-python.3.html) (F36, CO7, CO8)

## Todo
- […] __7za &hellip;
- […] rotate_dir
- […] cpal: CLI
- [ ] weekly
- [ ] monthly
- [ ] compress (daily)
- [ ] rsync_local
- [ ] backup_ftp
- [ ] backup_yadisk
