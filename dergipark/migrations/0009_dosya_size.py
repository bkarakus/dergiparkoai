# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-03 10:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dergipark', '0008_auto_20191203_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='dosya',
            name='size',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Dosya Boyutu'),
        ),
    ]
