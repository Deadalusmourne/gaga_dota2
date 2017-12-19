#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time    : 2017/11/24 
# __author__: caoge
import requests
import time
import platform
from logic import config
from utils import getMySqlConn

mysqld = getMySqlConn.MysqlConn(host=config.host, port=config.port, user=config.user, password=config.password, db=config.db)
url = 'http://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1?key=%s&appid=570'%config.API_TOKEN


def loop_current():
    req = requests.get(url)
    req = req.json()
    print(req)
    resp = req.get('response', '')
    if resp:
        result = resp.get('result', 1)
        count = resp.get('player_count', 1)
        if result:
            return count

def insert_data(mysqld):
    sql = "insert into logic_currentplayers (timeno, count_num) values (%s, %s)"
    timeno = time.time()
    req = loop_current()
    if req:
        print('current online players', req)
        result = mysqld.select(sql%(timeno, req))
        print('insert result', result)
    else:
        raise KeyError('insert error')


if __name__ == '__main__':
    insert_data(mysqld)