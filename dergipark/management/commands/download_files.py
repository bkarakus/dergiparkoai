# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

from dergipark.tasks import download_files


class Command(BaseCommand):
    help = 'Dergipark sitesinden kurum dergilerine ait makale ve dosyalarını indirir'

    def handle(self, *args, **options):
        self.stdout.write(u"Makalelere ait dosyalar indiriliyor")
        download_files(self.stdout)
