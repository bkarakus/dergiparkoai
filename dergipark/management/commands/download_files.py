import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.files.move import file_move_safe

from dergipark.models import Dergi, Makale, Sayi, Dosya, Yazar
from dergipark.utils import download_file

MEDIA_ROOT = settings.MEDIA_ROOT
MAKALE_DIR = os.path.join(MEDIA_ROOT, 'makaleler')


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        for dosya in Dosya.objects.filter(dosya__isnull=True):
            self.stdout.write(self.style.WARNING('"%s" indiriliyor' % dosya.url))
            path = download_file(dosya.url)
            if path is not None:
                filename = "{}.pdf".format(dosya.url.split('/')[-1])
                target_path = os.path.join(MAKALE_DIR, filename)
                relative_path = os.path.join('makaleler', filename)
                file_move_safe(path, target_path)
                dosya.dosya = relative_path
                dosya.save()
