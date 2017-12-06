#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time    : 2017/11/29 
# __author__: caoge
from logic import config
import requests
import os


def download_file(fileurl, filename):
    file_path = os.path.join('../static/ugc_icon/', filename)
    print(file_path)
    req = requests.get(fileurl, stream=True)
    if req.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in req:
                f.write(chunk)
        return file_path
    else:
        return 0


def get_file_info(ugcid):
    print(config.ugc_url)
    req = requests.get(config.ugc_url.format(ugcid=ugcid), stream=True)
    if req.status_code == 200:
        req_json = req.json()
        filename = req_json.get('data', {}).get('filename', '')
        fileurl = req_json.get('data', {}).get('url', '')
        if filename and fileurl:
            return download_file(fileurl, filename)
    else:
        return 0

get_file_info(46499322609643214)