#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time    : 2017/11/10 
# __author__: caoge
API_TOKEN = '79D1B68E3619897260FA6F5758C96005'

# 过去实时在线人数的历史数据月份
online_delay = -30

# mysql设置
host = '127.0.0.1'
port = 3306
db = 'gaga_dota2'
user = 'root'
password = '111111'

# 循环获取在线人数间隔
loop_get_cplayers = 300

appid = 570
# ugc file
ugc_url = "http://api.steampowered.com/ISteamRemoteStorage/GetUGCFileDetails/v1/?key=%s&ugcid={ugcid}&appid=%s"%(API_TOKEN, appid)

# # team icon path
# team_icon_path = '/static/ugc_icon/'


