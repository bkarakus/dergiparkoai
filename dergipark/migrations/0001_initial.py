# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-29 20:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dergi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dergi_adi', models.CharField(max_length=150, verbose_name='Dergi Ad\u0131')),
                ('oai_url', models.CharField(default='https://dergipark.org.tr/api/public/oai/', max_length=200, verbose_name='OAI URL')),
                ('set_name', models.CharField(max_length=50, verbose_name='Set Ad\u0131')),
            ],
            options={
                'verbose_name': 'Dergi',
                'verbose_name_plural': 'Dergiler',
            },
        ),
        migrations.CreateModel(
            name='Dosya',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=150, verbose_name='Dosya Adresi')),
            ],
            options={
                'verbose_name': 'Dosya',
                'verbose_name_plural': 'Dosyalar',
            },
        ),
        migrations.CreateModel(
            name='Makale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=150, unique=True, verbose_name='OAI Identifier')),
                ('datestamp', models.DateField(verbose_name='Datestamp')),
                ('title_tr', models.CharField(max_length=250, verbose_name='Ba\u015fl\u0131k [TR]')),
                ('title_en', models.CharField(max_length=250, verbose_name='Ba\u015fl\u0131k [EN]')),
                ('description_tr', models.TextField(verbose_name='A\xe7\u0131klama [TR]')),
                ('description_en', models.TextField(verbose_name='A\xe7\u0131klama [EN]')),
                ('subject_tr', models.CharField(max_length=250, verbose_name='Anahtar Kelimeler [TR]')),
                ('subject_en', models.CharField(max_length=250, verbose_name='Anahtar Kelimeler [EN]')),
                ('language', models.CharField(blank=True, max_length=10, verbose_name='Dil')),
                ('publisher', models.CharField(max_length=100, verbose_name='Yay\u0131nc\u0131')),
                ('dergi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dergipark.Dergi', verbose_name='Dergi')),
            ],
            options={
                'verbose_name': 'Makale',
                'verbose_name_plural': 'Makaleler',
            },
        ),
        migrations.CreateModel(
            name='Sayi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cilt_no', models.PositiveIntegerField(verbose_name='Cilt No')),
                ('sayi_no', models.PositiveIntegerField(verbose_name='Say\u0131 No')),
                ('dergi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dergipark.Dergi', verbose_name='Dergi')),
            ],
            options={
                'verbose_name': 'Say\u0131',
                'verbose_name_plural': 'Say\u0131lar',
            },
        ),
        migrations.CreateModel(
            name='Yazar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yazar_adi', models.CharField(max_length=50, verbose_name='Yazar Ad\u0131')),
                ('makale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dergipark.Makale', verbose_name='Makale')),
            ],
            options={
                'verbose_name': 'Yazar',
                'verbose_name_plural': 'Yazarlar',
            },
        ),
        migrations.AddField(
            model_name='makale',
            name='sayi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dergipark.Sayi', verbose_name='Say\u0131'),
        ),
        migrations.AddField(
            model_name='dosya',
            name='makale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dergipark.Makale', verbose_name='Makale'),
        ),
        migrations.AlterUniqueTogether(
            name='dergi',
            unique_together=set([('oai_url', 'set_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='sayi',
            unique_together=set([('dergi', 'cilt_no', 'sayi_no')]),
        ),
    ]
