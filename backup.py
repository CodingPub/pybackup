#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from utility import *


def backup(src, dst_dir, retemtion_days, hours_last_day=None):
    if hours_last_day is None:
        hours_last_day = 8

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
            if days >= 1:
                if days in retemtion_days:
                    if dt.hour < 23:
                        should_delete = True
                else:
                    should_delete = True
            elif days == 0 and dt.hour < 23 and (datetime.datetime.now() - dt).seconds > hours_last_day * 60 * 60:
                should_delete = True
            if should_delete:
                file = joinPaths(dst_dir, x)
                remove(file)


if __name__ == '__main__':
    if isDebug():
        for day in range(0, 18):
            for hour in range(0, 24):
                path = '/tmp/backup/config_201705%02d%02d.json' % (26 - day, hour)
                replacefile('/Users/linxiaobin/Developer/python/backup/config.json', path)

    content = readfile(joinPaths(cmddir(), 'config.json'))
    arr = str2Json(content)
    if arr and len(arr) > 0:
        for x in arr:
            backup(x.get('src'), x.get('dst_dir'), x.get('retemtion_days'), hours_last_day=x.get('hours_last_day'))
