#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from utility import *


def backup(src, dst_dir, retemtion_days):
    name = filename(src) + '_' + datetime.datetime.now().strftime('%Y%m%d%H' + fileExtension(src))
    dst = joinPaths(dst_dir, name)
    print('backup %s to %s' % (src, dst))
    createdir(dst_dir)

    cmd = 'rsync -aE --progress %s %s' % (src, dst)
    systemCmd(cmd)

    # delete older backups
    arr = [x for x in listdir(dst_dir) if x != '.DS_Store']
    for x in arr:
        name = filename(x)
        t = name.split('_')
        if t and len(t) > 1:
            dt = datetime.datetime.strptime(t[1], '%Y%m%d%H')
            days = (datetime.datetime.now() - dt).days
            should_delete = False
            if days >= retemtion_days:
                should_delete = True
            elif days >= 1 and dt.hour >= 1:
                should_delete = True
            if should_delete:
                file = joinPaths(dst_dir, x)
                remove(file)


if __name__ == '__main__':
    content = readfile(joinPaths(cmddir(), 'config.json'))
    arr = str2Json(content)
    if arr and len(arr) > 0:
        for x in arr:
            backup(x.get('src'), x.get('dst_dir'), x.get('retemtion_days'))
