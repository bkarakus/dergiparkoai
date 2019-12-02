# -*- coding: utf-8 -*-
import os
import csv
import commands
from shutil import copyfile

from django.conf import settings
from django.core.management.base import BaseCommand

from dergipark.models import Sayi

MEDIA_ROOT = settings.MEDIA_ROOT
SAFBULDER_DIR = os.path.join(settings.BASE_DIR, 'site_media', 'safbuilder')
SAFBUILDER_CMD_DIR = os.path.join(settings.BASE_DIR, 'SAFBuilder')
SAFBUILDER_CMD = './safbuilder.sh'


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(u'Sayılar için dspace dosyaları oluşturuluyor.'))
        for sayi in Sayi.objects.all():
            self.stdout.write(self.style.WARNING(
                u'{} Sayısı için dspace csv dosyası oluşturuluyor.'.format(sayi)
            ))
            dirname = "{}_cilt-{}_sayi-{}".format(sayi.dergi.set_name, sayi.cilt_no, sayi.sayi_no)
            working_dir = os.path.join(
                SAFBULDER_DIR, dirname
            )
            if not os.path.exists(working_dir):
                os.makedirs(working_dir)
            csv_file_path = os.path.join(working_dir, 'output.csv')
            with open(csv_file_path, mode='w') as csv_file:
                fieldnames = ['filename', 'dc.title', 'dc.contributor', 'dc.date.issued', 'dc.description']
                writer = csv.DictWriter(csv_file, delimiter=',', quotechar='"', fieldnames=fieldnames)

                writer.writeheader()
                for makale in sayi.makale_set.all():
                    if makale.dosya_set.count():
                        dosya = makale.dosya_set.first()
                        filename = os.path.basename(dosya.dosya.name)
                        dest_filename = os.path.join(working_dir, filename)
                        try:
                            copyfile(dosya.dosya.path, dest_filename)
                        except ValueError:
                            pass
                        else:
                            writer.writerow({
                                'filename': filename,
                                'dc.title': makale.title_tr.encode('utf8'),
                                'dc.contributor': '||'.join(yazar.yazar_adi for yazar in makale.yazar_set.all()).encode('utf8'),
                                'dc.date.issued': makale.datestamp.strftime("%m/%d/%Y") if makale.datestamp else '',
                                'dc.description': makale.description_tr.encode('utf8')
                            })

                os.chdir(SAFBUILDER_CMD_DIR)
                command = "{safbuilder_cmd} -c {csvfile} -o {dirname} -z".format(
                    safbuilder_cmd=SAFBUILDER_CMD, csvfile=csv_file_path, dirname=dirname
                )
                status, output = commands.getstatusoutput(command)
                if status == 0:
                    self.stdout.write(self.style.SUCCESS(
                        u'{} Sayısı için dspace import dosyası oluşturuldu.'.format(sayi)
                    ))
                else:
                    self.stdout.write(self.style.ERROR(
                        u'{} Sayısı için dspace import dosyası oluşturulamadı.\n'.format(sayi)
                    ))

