# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-18 12:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club_id', models.IntegerField(blank=True, db_index=True, default=None, null=True, unique=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('tag', models.CharField(max_length=128)),
                ('time_created', models.FloatField()),
                ('calibration_games_remaining', models.IntegerField(default=0)),
                ('logo', models.CharField(default='', max_length=256)),
                ('logo_sponsor', models.CharField(default='', max_length=256)),
                ('country', models.CharField(default='', max_length=20)),
                ('url', models.URLField()),
                ('games_played', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentPlayers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeno', models.FloatField()),
                ('count_num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='GameMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(unique=True)),
                ('description', models.CharField(max_length=128, verbose_name='匹配类型')),
            ],
        ),
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('name', models.CharField(max_length=64)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('localized_name', models.CharField(max_length=64)),
                ('url_small_portrait', models.URLField(default='')),
                ('url_large_portrait', models.URLField(default='')),
                ('url_full_portrait', models.URLField(default='')),
                ('url_vertical_portrait', models.URLField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('leagueid', models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(default='缺失名称', max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('tournament_url', models.URLField()),
                ('itemdef', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LobbyType',
            fields=[
                ('status', models.SmallIntegerField(primary_key=True, serialize=False, unique=True)),
                ('description', models.CharField(max_length=128, verbose_name='类型')),
            ],
        ),
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_id', models.BigIntegerField(db_index=True, unique=True)),
                ('match_seq_num', models.BigIntegerField(db_index=True)),
                ('start_time', models.FloatField(db_index=True)),
                ('series_id', models.IntegerField()),
                ('series_type', models.SmallIntegerField(choices=[(0, 'Non-series'), (1, 'BO3'), (1, 'BO5')], default=0)),
                ('players', models.TextField()),
                ('dire_team', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='dire_team', to='logic.Club')),
                ('league', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='logic.League')),
                ('lobby_type', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='logic.LobbyType')),
                ('radiant_team', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='radiant_team', to='logic.Club')),
            ],
        ),
        migrations.CreateModel(
            name='MatchToPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_slot', models.IntegerField()),
                ('hero_id', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='logic.Hero')),
                ('match_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='logic.Matches')),
            ],
        ),
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.IntegerField(auto_created=True, db_index=True, primary_key=True, serialize=False, unique=True)),
                ('account_id', models.BigIntegerField(db_index=True, unique=True)),
                ('steamid', models.CharField(default='', max_length=256)),
                ('communityvisibilitystate', models.SmallIntegerField(default=1)),
                ('lastlogoff', models.IntegerField(default=0)),
                ('avatar', models.URLField(default='')),
                ('avatarmedium', models.URLField(default='')),
                ('avatarfull', models.URLField(default='')),
                ('is_admin', models.SmallIntegerField(default=0)),
                ('club', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='logic.Club')),
            ],
        ),
        migrations.AddField(
            model_name='matchtoplayer',
            name='player_id',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='logic.Players'),
        ),
        migrations.AlterUniqueTogether(
            name='matchtoplayer',
            unique_together=set([('player_id', 'match_id')]),
        ),
    ]
