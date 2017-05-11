#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from utility import *


def backup(src, dst_dir, retemtion_days):
    name = filename(src) + '_' + datetime.datetime.now().strftime('%Y%m%d' + fileExtension(src))
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
            days = (datetime.datetime.now() - datetime.datetime.strptime(t[1], '%Y%m%d')).days
            if days >= retemtion_days:
                file = joinPaths(dst_dir, x)
                remove(file)


if __name__ == '__main__':
    content = readfile('config.json')
    arr = str2Json(content)
    if arr and len(arr) > 0:
        for x in arr:
            backup(x.get('src'), x.get('dst_dir'), x.get('retemtion_days'))
