#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time    : 2017/11/24 
# __author__: caoge
import datetime
import time
import traceback


def date_to_timeno(date_str, format_str='%Y-%m-%d %H:%M:%S'):
    if isinstance(date_str, datetime.datetime):
        timeno = time.mktime(date_str.timetuple())
    else:
        try:
            date_str = datetime.datetime.strptime(date_str, format_str)
            timeno = time.mktime(date_str.timetuple())
        except ValueError:
            print(traceback.format_exc())
            return ''
    return timeno


def timeno_to_date(timeno, format_str='%Y-%m-%d %H:%M:%S'):
    time_local = time.localtime(timeno)
    dt = time.strftime(format_str, time_local)
    return dt


# print(date_to_timeno('2017-02-12 12:12:12'))
# print(datetime.datetime('1486872732.0'))
# print(time.time(), type(time.time()))