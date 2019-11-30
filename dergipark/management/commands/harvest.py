import re
from datetime import datetime
from sickle import Sickle

from django.core.management.base import BaseCommand, CommandError

from dergipark.models import Dergi, Makale, Sayi, Dosya, Yazar
from dergipark.utils import download_file


def get_metadata_attr(metadata, attr_name, index):
    try:
        value = metadata[attr_name][index]
    except IndexError:
        value = ''
    except KeyError:
        value = ''
    return value


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        for dergi in Dergi.objects.all():
            sickle = Sickle(dergi.oai_url)
            records = sickle.ListRecords(metadataPrefix='oai_dc', set=dergi.set_name)
            i = 0
            for record in records:
                header = record.header
                metadata = record.metadata
                identifier = header.identifier
                datestamp_str = header.datestamp
                datestamp = datetime.strptime(datestamp_str, '%Y-%m-%dT%H:%M:%SZ')
                volume_issue = metadata['source'][0].replace('\n', '').strip()
                volume = re.findall('Volume: \d+', volume_issue)
                issue = re.findall('Issue: \d+', volume_issue)
                try:
                    cilt_no = int(re.findall('\d+', volume[0])[0])
                    sayi_no = int(re.findall('\d+', issue[0])[0])
                except IndexError:
                    i += 1
                else:
                    sayi, created = Sayi.objects.get_or_create(dergi=dergi, cilt_no=cilt_no, sayi_no=sayi_no)
                    makale, created = Makale.objects.get_or_create(dergi=dergi, sayi=sayi, identifier=identifier)
                    makale.title_tr = get_metadata_attr(metadata, 'title', 1)
                    makale.title_en = get_metadata_attr(metadata, 'title', 0)
                    makale.description_tr = get_metadata_attr(metadata, 'description', 1)
                    makale.description_en = get_metadata_attr(metadata, 'description', 0)
                    makale.subject_tr = get_metadata_attr(metadata, 'subject', 1)
                    makale.subject_en = get_metadata_attr(metadata, 'subject', 0)
                    makale.language = get_metadata_attr(metadata, 'language', 0)
                    makale.publisher = get_metadata_attr(metadata, 'publisher', 0)
                    makale.save()

                    if 'creator' in metadata:
                        for yazar in metadata['creator']:
                            yazar_adi = yazar.strip()
                            author, created = Yazar.objects.get_or_create(makale=makale, yazar_adi=yazar_adi)

                    if 'relation' in metadata:
                        for dosya_url in metadata['relation']:
                            dosya, created = Dosya.objects.get_or_create(makale=makale, url=dosya_url)

            self.stdout.write(self.style.ERROR('"%s" tane kayitta cilt no hatali' % i))
            self.stdout.write(self.style.SUCCESS('"%s" dergisi aktarildi' % dergi.dergi_adi))

        for dosya in Dosya.objects.all():
            download_file(dosya.url)
            break
