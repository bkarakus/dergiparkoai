# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

from dergipark.tasks import sync_sets


class Command(BaseCommand):
    help = 'Dergipark sitesinden kurum dergilerine ait makale ve dosyalarını indirir'

    def handle(self, *args, **options):
        self.stdout.write(u"Makalelere ait dosyalar indiriliyor")
        sync_sets(self.stdout)
