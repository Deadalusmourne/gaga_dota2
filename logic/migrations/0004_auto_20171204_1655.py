# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-04 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logic', '0003_auto_20171204_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='logo',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='club',
            name='logo_sponsor',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='players',
            name='steamid',
            field=models.CharField(default='', max_length=256),
        ),
    ]
