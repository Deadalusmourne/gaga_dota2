#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time    : 2017/12/12 
# __author__: caoge
from analysis import da_config
import requests
import json


def fast_write(db_type, data_list, table_name):
    url = da_config.FAST_WRITE_URL
    param = {
        'db_type': db_type,
        'coll_name': table_name,
        'data_list': data_list,
    }
    req = requests.post(url, data=json.dumps(param))
    print('fast_write req',req)
    return req









