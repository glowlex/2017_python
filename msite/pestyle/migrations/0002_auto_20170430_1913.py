# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-30 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pestyle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.IntegerField(default=524901),
        ),
    ]
