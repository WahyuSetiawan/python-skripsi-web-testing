# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-09 08:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20170609_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='valuedata',
            field=models.CharField(default='1', max_length=100),
        ),
        migrations.AlterField(
            model_name='setting',
            name='tag',
            field=models.CharField(default='1', max_length=100),
        ),
    ]
