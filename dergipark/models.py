# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Dergi(models.Model):
    dergi_adi = models.CharField('Dergi Adı', max_length=150)
    oai_url = models.CharField('OAI URL', max_length=200, default='https://dergipark.org.tr/api/public/oai/')
    set_name = models.CharField('Set Adı', max_length=50)

    def __unicode__(self):
        return self.dergi_adi

    class Meta:
        verbose_name = 'Dergi'
        verbose_name_plural = 'Dergiler'
        unique_together = ('oai_url', 'set_name')


class Sayi(models.Model):
    dergi = models.ForeignKey(Dergi, verbose_name='Dergi', on_delete=models.CASCADE)
    cilt_no = models.PositiveIntegerField('Cilt No')
    sayi_no = models.PositiveIntegerField('Sayı No')

    def __unicode__(self):
        return u'Cilt:{} Sayı:{}'.format(self.cilt_no, self.sayi_no)

    class Meta:
        verbose_name = 'Sayı'
        verbose_name_plural = 'Sayılar'
        unique_together = ('dergi', 'cilt_no', 'sayi_no')
        ordering = ('dergi', 'cilt_no', 'sayi_no')


class Makale(models.Model):
    dergi = models.ForeignKey(Dergi, verbose_name='Dergi', on_delete=models.CASCADE)
    sayi = models.ForeignKey(Sayi, verbose_name='Sayı', on_delete=models.CASCADE)
    identifier = models.CharField('OAI Identifier', max_length=150, unique=True)
    datestamp = models.DateField('Datestamp', null=True, blank=True)
    title_tr = models.CharField('Başlık [TR]', max_length=250, blank=True)
    title_en = models.CharField('Başlık [EN]', max_length=250, blank=True)
    description_tr = models.TextField('Açıklama [TR]', null=True, blank=True)
    description_en = models.TextField('Açıklama [EN]', null=True, blank=True)
    subject_tr = models.CharField('Anahtar Kelimeler [TR]', max_length=250, blank=True)
    subject_en = models.CharField('Anahtar Kelimeler [EN]', max_length=250, blank=True)
    language = models.CharField('Dil', max_length=10, blank=True)
    publisher = models.CharField('Yayıncı', max_length=100, blank=True)

    def __unicode__(self):
        return self.title_tr

    class Meta:
        verbose_name = 'Makale'
        verbose_name_plural = 'Makaleler'


class Yazar(models.Model):
    makale = models.ForeignKey(Makale, verbose_name='Makale', on_delete=models.CASCADE)
    yazar_adi = models.CharField('Yazar Adı', max_length=50)

    def __unicode__(self):
        return self.yazar_adi

    class Meta:
        verbose_name = 'Yazar'
        verbose_name_plural = 'Yazarlar'


class Dosya(models.Model):
    makale = models.ForeignKey(Makale, verbose_name='Makale', on_delete=models.CASCADE)
    url = models.URLField('Dosya Adresi', max_length=150)
    dosya = models.FileField(upload_to='makaleler', blank=True, null=True)

    class Meta:
        verbose_name = 'Dosya'
        verbose_name_plural = 'Dosyalar'
