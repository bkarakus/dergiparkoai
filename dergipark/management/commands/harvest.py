# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

from dergipark.tasks import harvest, download_files, build_saf_files, sync_sets, clean_yazar_adi


class Command(BaseCommand):
    help = 'Dergipark sitesinden kurum dergilerine ait makale ve dosyalarını indirir'

    def handle(self, *args, **options):
        self.stdout.write(u"Dergi setleri güncelleniyor")
        sync_sets(self.stdout)
        self.stdout.write(u"Yeni makaleler indiriliyor")
        harvest(self.stdout)
        self.stdout.write(u"Yazar isimleri düzenleniyor")
        clean_yazar_adi()
        self.stdout.write(u"Makalelere ait dosyalar indiriliyor")
        download_files(self.stdout)
        self.stdout.write(u"Dpsace arşiv dosyaları oluşturuluyor")
        build_saf_files(self.stdout)
