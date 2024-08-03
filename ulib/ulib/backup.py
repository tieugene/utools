#!/usr/bin/env python3
"""Main file"""
# 1. std
import sys
import pathlib
# 2. 3rd
import sh
# 3. local
import pre


# import vhost

def load_cfg() -> bool:
    try:
        data = pre.load_cfg('backup.ini')
        if data is None:
            sys.exit("Config not found")
    except pre.UlibCfgLoadError as e:
        sys.exit(str(e))


def mk_dir(path: pathlib.Path):
    # try to create folder if not exists
    ...


def rotate(path: pathlib.Path, count: int):
    # rotate subfolders
    ...


def guest_mount():
    # mount guest disk
    ...


def guest_umount():
    # umount guest disk
    ...


def rsync_local():
    ...
    # mount dest
    # rsync
    # umount


def cpal():
    # cp -al | mk hardlink
    ...


def backup_dir():
    # rsync -axAXH $addon --modify-window=1 --del --link-dest=
    ...


def __backup_1c():
    # for each subfolder:
    # 7za
    ...


def backup_1c7():
    # backup1C $1 $2 "1[Cc][Vv]7.?[Dd] *.[Dd][Bb][Ff]"
    ...


def backup_1c8():
    # backup1C $1 $2 "*"
    ...


def weekly() -> bool:
    ...
    # if today.weekday == 6
    # pack vdisks, dump self
    # cpal daily
    # rotate


def monthly() -> bool:
    ...
    # if today.day <= 7:
    # cpal weekly
    # rotate
