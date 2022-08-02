#!/usr/bin/env python3
"""HomeSnap - Duplicate backups"""

# 1. std
from typing import Optional
import os
import sys
import datetime
import logging
# 3. local
from ulib import pre, log, stamp, rsync, mail

# consts
DATIME_FMT = "%y-%m-%d %H:%M:%S"
MAIL_SUBJ = "HomeSnap sync: %s"
MAIL_BODY = "Beg: %s\nEnd: %s\n----\n%s"


def __now():
    return datetime.datetime.now().replace(microsecond=0)


def __handle_item(item: dict) -> Optional[tuple[bool, str]]:
    """Process one sync item.
    :return: None if update not started, True on update success, Error string if update started but not completed.
    :todo: async
    """
    name = item['name']
    retvalue = None
    try:
        # 3. chk stamps
        if (s_stamp := stamp.get_stamp(item['schk'])) is None:  # /misc/1tb/backup/ext
            return  # remote is busy yet
        d_stamp = stamp.get_stamp(item['dchk'])
        if s_stamp > (d_stamp or 0):  # 4. compare with local
            logging.info(f"{name}: Update required: Src ({s_stamp}) > Dst ({d_stamp})")
            # 5. rsync (linux: '-aqzAHX --del', macos: '-aqz'
            opts = item['opts'].split()
            rsync.rsync(opts + [item['spath'], item['dpath']])
            stamp.set_stamp(item['dchk'], s_stamp)  # 6. resume
            retvalue = (True, None)
            if epath := item.get('epath'):
                if os.path.isdir(epath):
                    try:
                        rsync.rsync(opts + [item['dpath'], epath])
                    except rsync.UlibRsyncError as e:
                        retvalue = (True, str(e))
                else:
                    retvalue = (True, "no external drive")
        elif s_stamp < (d_stamp or 0):
            logging.warning(f"{name}: Src stamp ({s_stamp}) < drc ({d_stamp})")
        else:  # stamps are equals => nothing to do
            logging.debug(f"{name}: Stamps are equal: {s_stamp}")
    except stamp.UlibGetStampError:  # sync not started
        # logging.warning(f"Item '{name}': {str(e)}")
        pass
    except (rsync.UlibRsyncError, stamp.UlibSetStampError) as e:
        retvalue = (False, str(e))
    return retvalue


def main():
    """Main procedure."""
    t0 = __now()
    mail_queue = []
    total = True
    try:
        if (data := pre.load_cfg('homesnap.json')) is None:   # 1. load cfg
            sys.exit("Config not found")
    except pre.UlibCfgLoadError as e:
        sys.exit(str(e))
    # 2. setup logger
    log.setLogger(data.get('log', 0))
    for item in data['items']:          # -. for each host:
        if updating := __handle_item(item):
            if updating[0]:
                msg = f"{item['name']}: OK"
                if updating[1]:
                    msg += f" ({updating[1]})"
            else:
                msg = f"{item['name']}: Err: {updating[1]}"
                total = False
            mail_queue.append(msg)
    if mail_queue:         # 7. mail result
        cfg = data['mail']
        mail.send_mail(
            smtp=cfg['smtp'],
            mailfrom=cfg['mailfrom'],
            creditentials=(cfg['mailfrom'], cfg['mailpass']),
            mailto=cfg['mailto'],
            subj=MAIL_SUBJ % ("Error", "OK")[int(total)],
            body=MAIL_BODY % (t0.isoformat(), __now().isoformat(), "\n".join(mail_queue))
        )


if __name__ == '__main__':
    main()
