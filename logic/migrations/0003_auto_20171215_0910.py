# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-15 09:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logic', '0002_auto_20171215_0627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matches',
            name='match_seq_num',
            field=models.BigIntegerField(db_index=True),
        ),
    ]