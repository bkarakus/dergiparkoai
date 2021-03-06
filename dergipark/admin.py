# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.utils import timezone
from django.http import Http404, HttpResponse
from django.template import Template, Context

from .models import Dergi, DergiSet, Makale, Yazar, Dosya, BatchImport
from .forms import BatchImportAddForm, BatchImportForm

SAFBULDER_DIR = os.path.join(settings.BASE_DIR, 'site_media', 'safbuilder')


class YazarInline(admin.TabularInline):
    model = Yazar


class DosyaInline(admin.TabularInline):
    model = Dosya


class DergiAdmin(admin.ModelAdmin):
    list_display = ('dergi_adi', 'oai_url', 'set_name')


class BatchImportAdmin(admin.ModelAdmin):
    list_display = ('dergi', 'olusturma_tarihi', 'download_link', 'import_edildi', 'import_edilme_tarihi')
    # form = BatchImportForm
    # add_form = BatchImportAddForm
    readonly_fields = ('dergi', 'olusturma_tarihi', 'import_edildi', 'import_edilme_tarihi', )
    actions = ['make_imported']

    def get_urls(self):
        urls = super(BatchImportAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<obj_id>\d+)/download/$', self.download, name="batchimport_download"),
        ]
        return my_urls + urls

    def make_imported(self, request, queryset):
        queryset.update(import_edildi=True)

    make_imported.short_description = "Dspace'e aktarıldı olarak işaretle"

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super(BatchImportAdmin, self).get_form(request, obj, **defaults)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        else:
            return super(BatchImportAdmin, self).get_readonly_fields(request, obj)

    def download_link(self, obj):
        template = Template('''
        <span class="download">
            <a href="{% url 'admin:batchimport_download' obj.pk %}">İndir (SimpleArchiveFormat)</a>
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
            batchimport = BatchImport.objects.get(pk=obj_id)
        except BatchImport.DoesNotExist:
            raise Http404
        else:
            batchimport.import_edildi = True
            batchimport.import_edilme_tarihi = timezone.now()
            dirname = "{}_{}".format(batchimport.dergi.set_name, batchimport.olusturma_tarihi.strftime('%Y-%m-%d'))
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
    list_display = ('dergi', 'title_tr', 'title_en')
    list_filter = ('dergi_set', )
    search_fields = ('title_tr', 'title_en',)
    inlines = [YazarInline, DosyaInline]


class DosyaAdmin(admin.ModelAdmin):
    list_display = ('url', 'dosya', 'mimetype')
    list_filter = ('mimetype',)


class YazarAdmin(admin.ModelAdmin):
    list_display = ('yazar_adi', 'cleaned_yazar_adi',)
    list_per_page = 250
    search_fields = ('yazar_adi_clean',)


class DergiSetAdmin(admin.ModelAdmin):
    list_display = ('dergi', 'set_id', 'set_name', 'import_to_dspace')
    list_filter = ('dergi', 'import_to_dspace',)


# Register your models here.
admin.site.register(DergiSet, DergiSetAdmin)
admin.site.register(Dergi, DergiAdmin)
admin.site.register(BatchImport, BatchImportAdmin)
admin.site.register(Makale, MakaleAdmin)
# admin.site.register(Dosya, DosyaAdmin)
# admin.site.register(Yazar, YazarAdmin)

