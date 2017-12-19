#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time    : 2017/11/27 
# __author__: caoge
from logic import config
import dota2api
import json
import requests
api = dota2api.Initialise(config.API_TOKEN, language='Zh-cn')
# req = api.get_live_league_games()
# with open('ttt.json', 'w') as f:
#     f.write(json.dumps(req))

# req = api.get_league_listing()
# print(req)
# for i in req['leagues']:
#     print(i['name'], i['leagueid'])

# req = api.get_top_live_games()
# print(req)

# req = api.get_match_history(league_id=5637, start_at_match_id=3456535005)
# req = api.get_match_history(league_id=5582)
# print(req)
#
# req = api.get_match_details(match_id=3583359836)
# print(req)

# req = api.get_team_info_by_team_id(start_at_team_id=726228, teams_requested=1)
# print(req)
# print(len(req['teams']))


'''
http://api.steampowered.com/IDOTA2Match_570/GetTeamInfoByTeamID/v1?key=79D1B68E3619897260FA6F5758C96005&team_id=1838315

'''
# req = api.get_team_info_by_team_id(start_at_team_id=1838315, teams_requested=1)
# result = req
# print(req)

# ugc_url = "http://api.steampowered.com/ISteamRemoteStorage/GetUGCFileDetails/v1/?key=79D1B68E3619897260FA6F5758C96005&ugcid=46499322609643214"
#
# req = requests.get("http://cloud-3.steamusercontent.com/ugc/46499322609643214/B5909AD7E90C90C7FD5BE12175504FC271987D9F/", stream=True)
# print(req)
# with open('ttt.png', 'wb') as f:
#     for chunk in req:
#         f.write(chunk)


# import pycountry
# print(list(pycountry.countries)[123])

# req = pycountry.subdivisions.get(country_code="UA")
# print(req)

# ge = pycountry.countries.get(alpha_2='CN')
# print(ge)

# req = api.get_player_summaries([133973515,])
# print(req)


# def convert_to_64_bit(number):
#     min64b = 76561197960265728
#     if number < min64b:
#         return number + min64b
#     return number
#
# base64_ids = list(map(convert_to_64_bit, filter(lambda x: x is not None, [138383546,])))
# print(base64_ids)


# my = 76561198098649274
# import time



# def turn_time(timeno):
#     print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timeno)))

# req = api.get_heroes()
# print(req)
