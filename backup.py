#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from utility import *


def backup(src, dst_dir, retemtion_days, hours_last_day=None):
    if hours_last_day is None:
        hours_last_day = 8
    
    name = Common.filename(src) + '-' + datetime.datetime.now().strftime('%Y%m%d%H' + Common.file_extension(src))
    dst = Common.join_paths(dst_dir, name)
    print('backup %s to %s' % (src, dst))
    Common.create_dir(dst_dir)

    cmd = 'rsync -aE --progress \"%s\" \"%s\"' % (src, dst)
    Common.system_cmd(cmd)

    # delete older backups
    files = Common.list_dir(dst_dir) 
    arr = [x for x in files if x != '.DS_Store']
    for x in arr:
        name = Common.filename(x)
        t = name.split('-')
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
                file = Common.join_paths(dst_dir, x)
                Common.remove(file)


if __name__ == '__main__':
    if Common.debug():
        for day in range(0, 18):
            for hour in range(0, 24):
                path = '/tmp/backup/config_201705%02d%02d.json' % (26 - day, hour)
                Common.replace_file('/Users/linxiaobin/Developer/python/backup/config.json', path)

    content = Common.read_file(Common.join_paths(Common.get_cmd_dir(), 'config.json'))
    arr = Common.str2json(content)
    if arr and len(arr) > 0:
        for x in arr:
            backup(x.get('src'), x.get('dst_dir'), x.get('retemtion_days'), hours_last_day=x.get('hours_last_day'))
