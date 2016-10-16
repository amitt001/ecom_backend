# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-16 07:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=30)),
                ('pin_code', models.CharField(max_length=6)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=30)),
                ('country', models.CharField(max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(max_length=5)),
                ('mobile_no', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='phone',
            unique_together=set([('user', 'mobile_no')]),
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set([('user', 'address')]),
        ),
    ]
