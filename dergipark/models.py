# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from utils import unicode_tr

# Create your models here.


class Dergi(models.Model):
    dergi_adi = models.CharField('Dergi Adı', max_length=150)
    oai_url = models.CharField('OAI URL', max_length=200, default='https://dergipark.org.tr/api/public/oai/')
    set_name = models.CharField('Set Adı', max_length=50)
    son_calisma = models.DateTimeField(verbose_name=u'Son Çalışma Zamanı', blank=True, null=True)

    def __unicode__(self):
        return self.dergi_adi

    class Meta:
        verbose_name = 'Dergi'
        verbose_name_plural = 'Dergiler'
        unique_together = ('oai_url', 'set_name')


class BatchImport(models.Model):
    dergi = models.ForeignKey(Dergi, verbose_name=u'Dergi', on_delete=models.CASCADE)
    olusturma_tarihi = models.DateTimeField(u'Oluşturma Tarihi', auto_now_add=True)
    import_edildi = models.BooleanField(u"Dspace'e Aktarıldı", default=False)
    import_edilme_tarihi = models.DateTimeField(u"Dspace'e Aktarılma Zamanı", blank=True, null=True)

    class Meta:
        verbose_name = "Dspace'e Aktarma Dosyası"
        verbose_name_plural = "Dspace'e Aktarma Dosyaları"


class Makale(models.Model):
    dergi = models.ForeignKey(Dergi, on_delete=models.CASCADE)
    batchimport = models.ForeignKey(
        BatchImport,
        verbose_name="Dspace'e Aktarma Dosyası",
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
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
    yazar_adi = models.CharField('Yazar Adı', max_length=150)
    yazar_adi_clean = models.CharField('Yazar Adı (Dspace)', max_length=150, blank=True)

    def __unicode__(self):
        return self.yazar_adi

    class Meta:
        verbose_name = 'Yazar'
        verbose_name_plural = 'Yazarlar'

    def clean_yazar_adi(self):
        unvanlar = ['dr.', 'yrd.', 'doç.', 'prof.', 'arş.', 'gör.', 'öğr.', 'ögr.',
                    'Dr.', 'Yrd.', 'Doç.', 'Prof.', 'Arş.', 'Gör.', 'Öğr.', 'Ögr.']
        yazar_adi = self.yazar_adi.split(';')[0].strip()

        for unvan in unvanlar:
            if unvan in yazar_adi:
                yazar_adi = yazar_adi.replace(unvan, '')

        if '-,' in yazar_adi:
            yazar_adi = yazar_adi.replace('-,', '')

        yazar_adi = yazar_adi.strip(',')
        yazar_adi = yazar_adi.strip()
        return unicode_tr(yazar_adi).title()


class Dosya(models.Model):
    makale = models.ForeignKey(Makale, verbose_name='Makale', on_delete=models.CASCADE)
    url = models.URLField('Dosya Adresi', max_length=150)
    mimetype = models.CharField(u'Dosya Tipi', max_length=50, blank=True)
    dosya = models.FileField(upload_to='makaleler', blank=True, null=True)
    size = models.PositiveIntegerField('Dosya Boyutu', default=0, editable=False)

    class Meta:
        verbose_name = 'Dosya'
        verbose_name_plural = 'Dosyalar'
