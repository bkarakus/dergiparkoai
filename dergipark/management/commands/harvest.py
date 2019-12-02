import re
from datetime import datetime
from sickle import Sickle

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from dergipark.models import Dergi, Makale, Sayi, Dosya, Yazar


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
            if dergi.son_calisma:
                son_calisma = dergi.son_calisma.strftime('%Y-%m-%d')
            else:
                son_calisma = '1970-01-01'
            #records = sickle.ListRecords(**{'metadataPrefix': 'oai_dc', 'set': dergi.set_name, 'from': son_calisma})
            records = sickle.ListRecords(metadataPrefix='oai_dc', set=dergi.set_name)
            i = 0
            for record in records:
                header = record.header
                metadata = record.metadata
                identifier = header.identifier
                datestamp_str = header.datestamp
                datestamp = datetime.strptime(datestamp_str, '%Y-%m-%dT%H:%M:%SZ')
                volume_issue = metadata['source'][0]
                match = re.search(r"Volume:(\s)?(?P<volume>(\d+)?),(\s)?Issue:(\s)?(?P<issue>(\d+)?)", volume_issue)
                if not match:
                    print volume_issue
                    i += 1
                else:
                    try:
                        cilt_no = int(match.group('volume'))
                    except:
                        cilt_no = 0
                    try:
                        sayi_no = int(match.group('issue'))
                    except:
                        sayi_no = 0
                    if sayi_no > 10:
                        print volume_issue
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
                            dosya.mimetype = get_metadata_attr(metadata, 'format', 0)
                            dosya.save()
            dergi.son_calisma = timezone.now()
            dergi.save()
            self.stdout.write(self.style.ERROR('"%s" tane kayitta cilt no hatali' % i))
            self.stdout.write(self.style.SUCCESS('"%s" dergisi aktarildi' % dergi.dergi_adi))
