# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-16 10:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homes', '0003_auto_20170816_0909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bread',
            name='grain',
        ),
    ]