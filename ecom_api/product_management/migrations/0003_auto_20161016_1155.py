# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-16 11:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0002_auto_20161016_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2016, 10, 16, 11, 55, 3, 390371, tzinfo=utc)),
        ),
    ]