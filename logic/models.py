from django.db import models
from logic import config
import requests
from init_doAPI import get_doAPI
import json
import time
import pycountry
from analysis import data_handler, da_config
# Create your models here.


class CurrentPlayers(models.Model):
    timeno = models.FloatField()
    count_num = models.IntegerField()

    @staticmethod
    def get_online():
        url = 'http://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1?key={key}&appid=570'.format(
            {'key': config.API_TOKEN})
        print(url)
        req = requests.get(url)
        req = req.json()
        resp = req.get('response', '')
        if resp:
            result = resp.get('result', 1)
            count = resp.get('player_count', 0)
            return count
        else:
            return ''


class League(models.Model):
    """
    联赛
    """
    leagueid = models.IntegerField(primary_key=True, db_index=True)
    name = models.CharField(max_length=255, default='缺失名称')
    description = models.TextField(blank=True, null=True)
    tournament_url = models.URLField()
    itemdef = models.IntegerField()

    @classmethod
    def update_league(cls):
        api = get_doAPI()
        L_list = api.get_league_listing()
        leagues = L_list['leagues'] if L_list else []
        for i_league in leagues:
            leagueid = i_league.get('leagueid', '')
            if leagueid:
                print('leagueid', leagueid)
                req = cls.objects.update_or_create(leagueid=leagueid, defaults=i_league)
                print(req)
            else:
                print(i_league)


class LobbyType(models.Model):
    """
    匹配类型 Solo queue;Public matchmaking
    """
    status = models.SmallIntegerField(unique=True, null=False, primary_key=True)
    description = models.CharField(max_length=128, verbose_name='类型')


class GameMode(models.Model):
    """
    游戏模式：all pick;random pick
    """
    value = models.SmallIntegerField(unique=True, null=False)
    description = models.CharField(max_length=128, verbose_name='匹配类型')


class Players(models.Model):
    account_id = models.BigIntegerField(unique=True, null=False, db_index=True)
    steamid = models.CharField(max_length=256, default='')
    communityvisibilitystate = models.SmallIntegerField(default=1)
    lastlogoff = models.IntegerField(default=0)
    avatar = models.URLField(default='')
    avatarmedium = models.URLField(default='')
    avatarfull = models.URLField(default='')
    club = models.ForeignKey(to="Club", null=True, blank=True, on_delete=None)
    is_admin = models.SmallIntegerField(default=0)


    @classmethod
    def get_or_create(cls, account_id, club='', is_admin=0, club_id=''):
        print('get_or_create')
        req = cls.objects.filter(account_id=account_id)
        if not req:
            api = get_doAPI()
            req2 = api.get_player_summaries(account_id)
            players = req2.get("players", [])
            if players:
                player = players[0]
                player['account_id'] = account_id
                insert_plyers = {
                    'account_id': account_id,
                    'steamid': player.get('steamid', ''),
                    'lastlogoff': player.get('lastlogoff', ''),
                    'avatar': player.get('avatar', ''),
                    'avatarmedium': player.get('avatarmedium', ''),
                    'avatarfull': player.get('avatarfull', ''),
                    'club': club,
                    'is_admin': is_admin
                }
                if not club: insert_plyers.pop('club')
                result = cls.objects.create(**insert_plyers)
                print(result)
                ## 发送到DA
                player['club_id'] = club_id
                player['is_admin'] = is_admin
                # 待考虑的roll back
                data_handler.fast_write(da_config.DB_LOGIC, player, 'players')
                ##
                req = cls.objects.filter(account_id=account_id)
        return req



    @classmethod
    def convert_to_64_bit(number):
        min64b = 76561197960265728
        if number < min64b:
            return number + min64b
        return number


class Club(models.Model):
    club_id = models.IntegerField(unique=True, null=True, db_index=True, blank=True, default=None)
    name = models.CharField(max_length=128, unique=True, null=False)
    tag = models.CharField(max_length=128)
    time_created = models.FloatField()
    calibration_games_remaining = models.IntegerField(default=0)
    logo = models.CharField(max_length=256, default='')
    logo_sponsor = models.CharField(max_length=256, default='')
    country = models.CharField(max_length=20,default='')
    url = models.URLField()
    games_played = models.IntegerField(default=0)

    @classmethod
    def add_one(cls, team_id):
        print('addd')
        api = get_doAPI()
        req = api.get_team_info_by_team_id(start_at_team_id=team_id, teams_requested=1)
        result = req
        print(req)
        if result.get('status', 0):
            team_list = result.get('teams', [])
            if team_list:
                team = team_list[0]
                country = pycountry.countries.get(alpha_2=str(team.get('country_code', '')).upper()) if team.get('country_code', '') else ''
                country = country.name if country else ''
                update_content = {
                    'club_id': team_id,
                    'name': team.get('name'),
                    'tag': team.get('tag', ''),
                    'time_created': team.get('time_created', 0),
                    'calibration_games_remaining': team.get('calibration_games_remaining', 0),
                    'logo': team.get('logo', 0),
                    'logo_sponsor': team.get('logo_sponsor', 0),
                    'country': country,
                    'url': team.get('url', ''),
                    'games_played': team.get('games_played', ''),
                }
                ### 创建队员如果没有
                print('update_content', update_content)
                req = cls.objects.update_or_create(name=team.get('name'), defaults=update_content)
                print('req__', req)
                # result_team = cls.objects.filter(club_id=team_id)
                # update team players
                players_ids, admin_id = get_player_from_team(team)
                Players.get_or_create(admin_id, club=req[0], is_admin=1, club_id=team_id)
                for account_id in players_ids:
                    Players.get_or_create(account_id, club=req[0], club_id=team_id)
                return req


def get_player_from_team(team):
    print('get_player_from_team')
    str1 = 'player_'
    str2 = '_account_id'
    start_num = 0
    players_list = []
    while True:
        di_team = str(start_num).join([str1, str2])
        player_id = team.get(di_team, '')
        if player_id:
            players_list.append(player_id)
        else:
            break
        start_num += 1
    return players_list, team.get('admin_account_id', '')


series_dict = ((0, 'Non-series'),
                (1, 'BO3'),
                (2, 'BO5'),
                )


class Matches(models.Model):
    match_id = models.BigIntegerField(unique=True, null=False, db_index=True)
    match_seq_num = models.BigIntegerField(db_index=True)
    start_time = models.FloatField(db_index=True)
    series_id = models.IntegerField()
    series_type = models.SmallIntegerField(choices=series_dict, default=0)
    lobby_type = models.ForeignKey(to="LobbyType", on_delete=None, db_constraint=False)
    radiant_team = models.ForeignKey(to="Club", related_name='radiant_team', on_delete=None, db_constraint=False) # 若是通过club反向查找match，可以截止club.objects.first().radiant_team
    dire_team = models.ForeignKey(to="Club", related_name='dire_team', on_delete=None, db_constraint=False)
    league = models.ForeignKey(to="League", null=True, on_delete=None, db_constraint=False)
    players = models.TextField()

    @classmethod
    def update_data(cls, league_id):
        print('start update league matches', league_id)
        if league_id:
            api = get_doAPI()
            start_at_match_id = ''
            recheck_count = 0
            while True:
                req_api = api.get_match_history(league_id=league_id, start_at_match_id=start_at_match_id)
                if req_api.get('status', 0):
                    matches = req_api.get('matches', [])
                    for match in matches:
                        time.sleep(2)
                        match_id = match.get('match_id', '')
                        if match_id:
                            players = match.get('players')
                            match['players'] = json.dumps(players)
                            # add league
                            league_set = League.objects.filter(leagueid=league_id)
                            league = league_set[0] if league_set else None
                            match['league'] = league
                            # lobby type instance
                            num_lobby = match.get('lobby_type', -1)
                            lobby = LobbyType.objects.filter(status=int(num_lobby))
                            match['lobby_type'] = lobby[0]
                            # club 增加
                            radiant_team_id = match.pop('radiant_team_id')
                            dire_team_id = match.pop('dire_team_id')
                            team1 = Club.objects.filter(club_id=int(radiant_team_id))
                            team2 = Club.objects.filter(club_id=int(dire_team_id))
                            if not (team1 and team2):
                                team1 = Club.add_one(radiant_team_id)[0]
                                team2 = Club.add_one(dire_team_id)[0]
                            if team1:
                                match['radiant_team'] = team1 if isinstance(team1, Club) else team1[0]
                            if team2:
                                match['dire_team'] = team2 if isinstance(team2, Club) else team2[0]
                            req = cls.objects.update_or_create(match_id=match_id, defaults=match)
                            print(req)
                            MatchToPlayer.create_one_data(req[0], players)
                    this_num = len(matches)
                    total_results = req_api.get('total_results', 0)
                    results_remaining = req_api.get('results_remaining', 0)
                    start_at_match_id = matches[-1].get('match_id')
                    if results_remaining == 0:
                        print('update match done')
                        break
                else:
                    recheck_count += 1
                    if recheck_count > 3:
                        raise ValueError('api connect failed')



class MatchToPlayer(models.Model):
    player_id = models.ForeignKey(to="Players",  db_index=True, on_delete=None, db_constraint=False)
    match_id = models.ForeignKey(to="Matches",  db_index=True, on_delete=None, db_constraint=False)  # to field 导致这张表的int不够用
    hero_id = models.ForeignKey(to="Hero", null=True, on_delete=None, db_constraint=False)
    player_slot = models.IntegerField()

    @classmethod
    def create_one_data(cls, match, players):
        print("create_one_data")
        for item in players:
            player_id = item.get("account_id", 4294967295)
            hero = Hero.objects.filter(id=item.get("hero_id", 0))
            if hero:
                hero = hero[0]
            else:
                continue
            player = Players.get_or_create(player_id)
            if player:
                player = player if isinstance(player, Players) else player[0]
            else:
                continue
            cls.objects.get_or_create(**{
                "player_id": player,
                "match_id": match,
                "hero_id": hero,
                "player_slot": int(item.get("player_slot", 0))
            })

    class Meta:
        unique_together = ('player_id', 'match_id')


class Hero(models.Model):
    name = models.CharField(max_length=64, null=False)
    id = models.IntegerField(null=False, primary_key=True)
    localized_name = models.CharField(max_length=64)
    url_small_portrait = models.URLField(default='')
    url_large_portrait = models.URLField(default='')
    url_full_portrait = models.URLField(default='')
    url_vertical_portrait = models.URLField(default='')

    @classmethod
    def update_data(cls):
        api = get_doAPI()
        req = api.get_heroes()
        heroes = req.get("heroes", [])
        for i_hero in heroes:
            id_h = i_hero.get("id", 0)
            req2 = cls.objects.update_or_create(id=id_h, defaults=i_hero)
            print(req2)