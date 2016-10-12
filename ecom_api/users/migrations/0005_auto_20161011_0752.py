# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-11 07:52
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0004_auto_20161011_0648'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=30)),
                ('pin_code', models.CharField(max_length=6)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=30)),
                ('country', models.CharField(max_length=30)),
                ('country_code', models.CharField(max_length=5)),
                ('mobile_no', models.CharField(max_length=10)),
                ('created_on', models.DateField(default=datetime.datetime(2016, 10, 11, 7, 52, 0, 961432))),
                ('updated_on', models.DateField(default=datetime.datetime(2016, 10, 11, 7, 52, 0, 961471))),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='address',
            name='user',
        ),
        migrations.RemoveField(
            model_name='phone',
            name='user',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='Phone',
        ),
    ]
