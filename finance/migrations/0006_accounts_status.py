# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-14 10:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_auto_20170313_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='status',
            field=models.CharField(choices=[('I', 'Не используется'), ('A', 'Используется')], default='A', max_length=1),
        ),
    ]
