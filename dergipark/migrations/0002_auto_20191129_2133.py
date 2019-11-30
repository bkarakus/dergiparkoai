# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-29 21:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dergipark', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sayi',
            options={'ordering': ('dergi', 'cilt_no', 'sayi_no'), 'verbose_name': 'Say\u0131', 'verbose_name_plural': 'Say\u0131lar'},
        ),
        migrations.AlterField(
            model_name='makale',
            name='datestamp',
            field=models.DateField(blank=True, null=True, verbose_name='Datestamp'),
        ),
        migrations.AlterField(
            model_name='makale',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='A\xe7\u0131klama [EN]'),
        ),
        migrations.AlterField(
            model_name='makale',
            name='description_tr',
            field=models.TextField(blank=True, null=True, verbose_name='A\xe7\u0131klama [TR]'),
        ),
        migrations.AlterField(
            model_name='makale',
            name='publisher',
            field=models.CharField(blank=True, max_length=100, verbose_name='Yay\u0131nc\u0131'),
        ),
        migrations.AlterField(
            model_name='makale',
            name='subject_en',
            field=models.CharField(blank=True, max_length=250, verbose_name='Anahtar Kelimeler [EN]'),
        ),
        migrations.AlterField(
            model_name='makale',
            name='subject_tr',
            field=models.CharField(blank=True, max_length=250, verbose_name='Anahtar Kelimeler [TR]'),
        ),
        migrations.AlterField(
            model_name='makale',
            name='title_en',
            field=models.CharField(blank=True, max_length=250, verbose_name='Ba\u015fl\u0131k [EN]'),
        ),
        migrations.AlterField(
            model_name='makale',
            name='title_tr',
            field=models.CharField(blank=True, max_length=250, verbose_name='Ba\u015fl\u0131k [TR]'),
        ),
    ]
