# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.http import Http404, HttpResponse
from django.template import Template, Context

from dergipark.models import Dergi, Sayi, Makale, Yazar, Dosya

SAFBULDER_DIR = os.path.join(settings.BASE_DIR, 'site_media', 'safbuilder')


class YazarInline(admin.TabularInline):
    model = Yazar


class DosyaInline(admin.TabularInline):
    model = Dosya


class DergiAdmin(admin.ModelAdmin):
    list_display = ('dergi_adi', 'oai_url', 'set_name')


class SayiAdmin(admin.ModelAdmin):
    list_display = ('dergi', 'cilt_no', 'sayi_no', 'download_link')

    def get_urls(self):
        urls = super(SayiAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<obj_id>\d+)/download/$', self.download, name="sayi_download"),
        ]
        return my_urls + urls

    def download_link(self, obj):
        template = Template('''
        <span class="download">
            <a href="{% url 'admin:sayi_download' obj.pk %}">İndir (SimpleArchiveFormat)</a>
        </span>
        ''')
        context = Context({
            'obj': obj,
        })

        html = template.render(context)

        return html

    download_link.short_description = u'İndir (SimpleArchiveFormat)'
    download_link.allow_tags = True

    def download(self, request, obj_id):
        try:
            sayi = Sayi.objects.get(pk=obj_id)
        except Sayi.DoesNotExist:
            raise Http404
        else:
            dirname = "{}_cilt-{}_sayi-{}".format(sayi.dergi.set_name, sayi.cilt_no, sayi.sayi_no)
            file_dir = os.path.join(
                SAFBULDER_DIR,
                dirname,
            )
            file_path = os.path.join(file_dir, '{}.zip'.format(dirname))
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/force-download")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response
            raise Http404


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