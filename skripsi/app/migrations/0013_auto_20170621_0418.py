# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 21:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20170621_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testingdata',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
