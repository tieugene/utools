#!/usr/bin/env python3
"""Main file"""
# 1. std
import sys

# 2. local
import data
import mail
import pre
# import vhost


def main():
    if not pre.load_cfg('ulib.json'):
        sys.exit(1)
    mail.send_mail()
    return
    # pre.cli()
    for vhitem in data.Cfg['vhost']:
        vh = vhost.VHost(vhitem['name'])
        print(vh.getState())
        # chk state
        # freeze (if possible)
        # for drive in:
        # ... handle
        # unfreeze (if required)


if __name__ == '__main__':
    main()

'''
run: [1, 5]
suspend: [3, 1]
resume: [1, 5]
'''