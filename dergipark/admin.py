# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from dergipark.models import Dergi, Sayi, Makale, Yazar, Dosya


class YazarInline(admin.TabularInline):
    model = Yazar


class DosyaInline(admin.TabularInline):
    model = Dosya


class DergiAdmin(admin.ModelAdmin):
    list_display = ('dergi_adi', 'oai_url', 'set_name')


class SayiAdmin(admin.ModelAdmin):
    list_display = ('dergi', 'cilt_no', 'sayi_no')


class MakaleAdmin(admin.ModelAdmin):
    list_display = ('sayi', 'title_tr')
    list_filter = ('dergi', )
    inlines = [YazarInline, DosyaInline]


class DosyaAdmin(admin.ModelAdmin):
    list_display = ('url', 'dosya')


# Register your models here.
admin.site.register(Dergi, DergiAdmin)
admin.site.register(Sayi, SayiAdmin)
admin.site.register(Makale, MakaleAdmin)
admin.site.register(Dosya, DosyaAdmin)