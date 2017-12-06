from django.shortcuts import render, HttpResponse

# Create your views here.
import requests
import datetime
import json
from logic import config
from logic import models
from utils import deal_date
from init_doAPI import get_doAPI


def intime_online_person(requests):
    req_final = {'success': 0, 'resp': {}}
    if requests.method == 'GET':
        type_m = requests.GET.get('type', 'intimeCount')
        if type_m == 'intimeCount':
            req_num = models.CurrentPlayers.get_online()
            if req_num:
                req_final =  {'success': 1, 'resp': {'onlineCount': req_num}}
        elif type_m == 'historyData':
            delta_day = int(requests.GET.get('delta_day', config.online_delay))
            # c_players = models.CurrentPlayers()
            now_date = datetime.datetime.now()
            forward_date = now_date + datetime.timedelta(days=delta_day)
            timeno = deal_date.date_to_timeno(forward_date)
            # data_obj = c_players.objects.filter(timeno__gt=timeno)
            data_obj = models.CurrentPlayers.objects.filter().all()
            players_num_list = []
            for i_data in data_obj:
                timeno_one = i_data.timeno
                count_num = i_data.count_num
                # date_req = deal_date.timeno_to_date(timeno_one)
                date_req = timeno_one
                print('one', count_num, date_req)
                if count_num and date_req:
                    players_num_list.append([date_req, count_num])
            if players_num_list:
                req_final = {'success': 1, 'resp': {'historyData': players_num_list}}
            print(req_final)
    return HttpResponse(json.dumps(req_final))


def get_chart(request):
    return render(request, 'main.html')


def get_league_match_by_id(request, league_id):
    req_return = {'success': 0, 'resp': {}}
    if league_id:
        # 更新league表
        update_trigger = request.GET.get('update', 0)      # 0: 00, 1: 01, 2: 10 , 3: 11
        update_trigger_b = "{:b}".format(int(update_trigger))
        if len(update_trigger_b) == 1:
            update_trigger_b = ''.join(['0', update_trigger_b])
        trigger_league, trigger_match = update_trigger_b if len(update_trigger_b) == 2 else '00'
        print(trigger_league, trigger_match, update_trigger_b)
        if int(trigger_league):
            models.League.update_league()
        req = models.League.objects.get(leagueid=league_id)
        if req:
            if int(trigger_match):
                models.Matches.update_data(league_id)
            matches_req = models.Matches.objects.filter(league=req)
            return HttpResponse(json.dumps({"succ": 1, "resp": {"league": req, "matches": matches_req}}))
    return HttpResponse(json.dumps(req_return))


def go_test(request):
    from django.utils.translation import ugettext_lazy as _
    req = (_('Ukraine'))
    print(req)
    return HttpResponse(json.dumps(req))


def update_hero(request):
    models.Hero.update_data()
    return HttpResponse("gaga")