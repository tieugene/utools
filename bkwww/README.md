# waxa\_backup\_www

Backup web-sites of WaxaShop

## Requirements:
- `/usr/bin/mysqldump`
- `/usr/bin/rsync`
- `/usr/bin/zstd`
- `/usr/bin/mail`

## Files:

Files that are using for job:

- [`/usr/local/bin/bkwww.sh`](src/usr/local/bin/bkwww.sh) - main script
- [`/usr/local/etc/bkwww.conf`](src/usr/local/etc/bkwww.conf) - it's config (_sample_)
- [`~/.my.cnf`](src/my.cnf) - MySQL/MariaDB client config (_sample_)
- [`/usr/local/lib/bkwww_x.lst`](src/usr/local/lib/bkwww_x.lst) - dirs/files to exclude on backing up 
- [`/etc/cron.daily/z_bkwww`](src/etc/cron.daily/z_bkwww) - crond daily task
- [`/etc/logrotate.d/bkwww`](src/etc/logrotate.d/bkwww) (optional)
- `/var/log/bkwww.log` (creaiting during job, optional)

## Install

[RTFM](HOWTO.md)

# TODO

- rsync log
   Attach rsync -i to email
- stderr > $ERR | mail
   Log all stderr into $ERR and check | mail it at the end
- verbosity
   0: errors only, 1: short, 2: full (default)
