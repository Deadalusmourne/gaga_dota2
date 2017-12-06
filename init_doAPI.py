#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time    : 2017/11/27 
# __author__: caoge

import dota2api
from logic import config
import pickle
import traceback


def pick_into():
    api = dota2api.Initialise(config.API_TOKEN, language='Zh-cn')
    with open('row_data/doAPI.pickle', 'wb') as f:
        f.write(pickle.dumps(api))


def get_doAPI():
    try:
        with open('row_data/doAPI.pickle', 'rb') as f:
            api = pickle.loads(f.read())
    except (FileNotFoundError, TypeError):
        print(traceback.format_exc())
        api = dota2api.Initialise(config.API_TOKEN, language='Zh-cn')
    return api

if __name__ == '__main__':
    pick_into()