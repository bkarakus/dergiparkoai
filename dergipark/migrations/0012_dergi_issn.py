# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-19 12:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dergipark', '0011_auto_20191219_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='dergi',
            name='issn',
            field=models.CharField(blank=True, max_length=9, verbose_name='ISSN'),
        ),
    ]