# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-12 08:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0008_auto_20161012_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoes',
            name='created_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2016, 10, 12, 8, 29, 11, 548280)),
        ),
    ]
