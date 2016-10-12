# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-12 03:42
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shoes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('display_name', models.CharField(blank=True, max_length=300)),
                ('manufacturer', models.CharField(blank=True, max_length=200)),
                ('description', models.TextField(blank=True, default=b'', max_length=1000)),
                ('price', models.FloatField()),
                ('in_stock', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(blank=True, default=datetime.datetime(2016, 10, 12, 3, 42, 14, 844896))),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('seller_name', models.CharField(blank=True, max_length=100)),
                ('size', models.FloatField()),
                ('colour', models.CharField(max_length=10)),
                ('shoe_type', models.CharField(choices=[(b'Sports', b'SPORTS'), (b'Running', b'RUNNING'), (b'Casual', b'CASUAL'), (b'Formal', b'FORMAL'), (b'Mountaineering', b'MOUNTAINEERING')], default=b'CASUAL', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
