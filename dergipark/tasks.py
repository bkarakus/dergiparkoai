# -*- coding: utf-8 -*-
import os
import sys
import csv
import commands
from datetime import datetime
from sickle import Sickle
from shutil import copyfile

from django.utils import timezone
from django.conf import settings
from django.core.management.color import color_style
from django.core.files.move import file_move_safe
from django.db.models import Q

from dergipark.models import Dergi, Makale, Dosya, Yazar, BatchImport
from dergipark.utils import download_file

style = color_style()

MEDIA_ROOT = settings.MEDIA_ROOT
MAKALE_DIR = os.path.join(MEDIA_ROOT, 'makaleler')
MEDIA_ROOT = settings.MEDIA_ROOT
SAFBULDER_TARGET_DIR = settings.SAFBULDER_TARGET_DIR
SAFBUILDER_CMD_DIR = settings.SAFBUILDER_CMD_DIR
SAFBUILDER_CMD = settings.SAFBUILDER_CMD

FILENAME_MAPS = {
    'application/pdf': '.pdf',
    'application/msword': '.doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    'text/plain': '.txt'
}


def get_file_ext(content_tpye):
    if content_tpye in FILENAME_MAPS:
        return FILENAME_MAPS[content_tpye]
    return ''


def get_metadata_attr(metadata, attr_name, index):
    try:
        value = metadata[attr_name][index]
    except IndexError:
        value = ''
    except KeyError:
        value = ''
    return value


def clean_yazar_adi():
    for yazar in Yazar.objects.all():
        yazar.cleaned_yazar_adi = yazar.clean_yazar_adi()
        yazar.save()


def harvest(stdout=sys.stdout):
    for dergi in Dergi.objects.all():
        sickle = Sickle(dergi.oai_url)
        if dergi.son_calisma:
            son_calisma = dergi.son_calisma.strftime('%Y-%m-%d')
        else:
            son_calisma = '1970-01-01'
        # records = sickle.ListRecords(**{'metadataPrefix': 'oai_dc', 'set': dergi.set_name, 'from': son_calisma})
        records = sickle.ListRecords(metadataPrefix='oai_dc', set=dergi.set_name)
        for record in records:
            header = record.header
            metadata = record.metadata
            identifier = header.identifier
            datestamp_str = header.datestamp
            datestamp = datetime.strptime(datestamp_str, '%Y-%m-%dT%H:%M:%SZ')
            volume_issue = metadata['source'][0]
            makale, created = Makale.objects.get_or_create(dergi=dergi, identifier=identifier)
            makale.datestamp = datestamp
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
                    author.clenaed_yazar_adi = author.clean_yazar_adi()
                    author.save()

            if 'relation' in metadata:
                for dosya_url in metadata['relation']:
                    dosya, created = Dosya.objects.get_or_create(makale=makale, url=dosya_url)
                    dosya.save()

        dergi.son_calisma = timezone.now()
        dergi.save()
        stdout.write('"%s" dergisi aktarildi' % dergi.dergi_adi)


def download_files(stdout=sys.stdout):
    stdout.write('Dosyalar indiriliyor')
    for dosya in Dosya.objects.filter(Q(dosya__isnull=True) | Q(dosya='')):
        stdout.write('"%s" indiriliyor' % dosya.url)
        path, content_type = download_file(dosya.url)
        if path is not None:
            ext = get_file_ext(content_type)
            filename = "{filename}{ext}".format(filename=dosya.url.split('/')[-1], ext=ext)
            target_path = os.path.join(MAKALE_DIR, filename)
            relative_path = os.path.join('makaleler', filename)
            file_move_safe(path, target_path, allow_overwrite=True)
            dosya.dosya = relative_path
            dosya.size = dosya.dosya.size
            dosya.mimetype = content_type
            dosya.save()


def build_saf_files(stdout=sys.stdout):
    stdout.write(u'Dergiler için dspace dosyaları oluşturuluyor.')
    for dergi in Dergi.objects.all():
        qs = dergi.makale_set.filter(batchimport=None)
        if qs.exists():
            batchimport = BatchImport.objects.create(dergi=dergi)
            qs.update(batchimport=batchimport)

            stdout.write(u'{} Dergisi için dspace csv dosyası oluşturuluyor.'.format(dergi))
            dirname = "{}_{}".format(dergi.set_name, batchimport.olusturma_tarihi.strftime("%Y-%m-%d"))
            working_dir = os.path.join(
                SAFBULDER_TARGET_DIR, dirname
            )
            if not os.path.exists(working_dir):
                os.makedirs(working_dir)
            csv_file_path = os.path.join(working_dir, 'output.csv')
            with open(csv_file_path, mode='w') as csv_file:
                fieldnames = [
                    'filename',
                    'dc.contributor.author',
                    'dc.date',
                    'dc.date.accessioned',
                    'dc.date.available',
                    'dc.date.issued',
                    'dc.description.abstract[tr_TR]',
                    'dc.description[tr_TR]',
                    'dc.identifier',
                    'dc.identifier.issn',
                    'dc.language.iso[tr_TR]',
                    'dc.publisher[tr_TR]',
                    'dc.relation',
                    'dc.relation.ispartofseries',
                    'dc.relation.publicationcategory[tr_TR]',
                    'dc.rights[tr_TR]',
                    'dc.subject[tr_TR]',
                    'dc.title.alternative[tr_TR]',
                    'dc.title[tr_TR]',
                    'dc.type[tr_TR]',
                ]
                writer = csv.DictWriter(csv_file, delimiter=',', quotechar='"', fieldnames=fieldnames)

                writer.writeheader()
                for makale in batchimport.makale_set.all():
                    if makale.dosya_set.filter(size__gt=0).count():
                        filenames = []
                        relations = []
                        for dosya in makale.dosya_set.filter(size__gt=0):
                            filename = os.path.basename(dosya.dosya.name)
                            dest_filename = os.path.join(working_dir, filename)
                            try:
                                copyfile(dosya.dosya.path, dest_filename)
                            except ValueError:
                                pass
                            else:
                                filenames.append(filename)
                                relations.append(dosya.url)
                        if filenames:
                            formatted_date = ''
                            if makale.datestamp:
                                formatted_date = makale.datestamp.strftime("%Y-%m-%dT%H:%M:%SZ")

                            writer.writerow({
                                'filename': '||'.join(filenames),
                                'dc.contributor.author': '||'.join(
                                    y.cleaned_yazar_adi for y in makale.yazar_set.all()
                                ).encode('utf8'),
                                'dc.date': formatted_date,
                                'dc.date.accessioned': formatted_date,
                                'dc.date.available': formatted_date,
                                'dc.date.issued': makale.datestamp.strftime("%m/%d/%Y") if makale.datestamp else '',
                                'dc.description.abstract[tr_TR]': '\n'.join(
                                    [makale.description_tr, makale.description_en]
                                ).encode('utf8'),
                                'dc.description[tr_TR]': makale.title_en.encode('utf8'),
                                'dc.identifier': makale.identifier,
                                'dc.identifier.issn': makale.dergi.issn,
                                'dc.language.iso[tr_TR]': makale.language,
                                'dc.publisher[tr_TR]': makale.dergi.dergi_adi.encode('utf8'),
                                'dc.relation': '||'.join(relations),
                                'dc.relation.ispartofseries': '',
                                'dc.relation.publicationcategory[tr_TR]': u'Ulusal Yayın'.encode('utf8'),
                                'dc.rights[tr_TR]': 'info:eu-repo/semantics/openAccess',
                                'dc.subject[tr_TR]': '||'.join(
                                    [makale.subject_tr, makale.subject_en]
                                ).encode('utf8'),
                                'dc.title.alternative[tr_TR]': makale.title_en.encode('utf8'),
                                'dc.title[tr_TR]': makale.title_tr.encode('utf8'),
                                'dc.type[tr_TR]': 'Article',
                            })

                os.chdir(SAFBUILDER_CMD_DIR)
                command = "{safbuilder_cmd} -c {csvfile} -o {dirname} -z".format(
                    safbuilder_cmd=SAFBUILDER_CMD, csvfile=csv_file_path, dirname=dirname
                )
                status, output = commands.getstatusoutput(command)
                if status == 0:
                    stdout.write(
                        u'{} dergisi için dspace import dosyası oluşturuldu.'.format(dergi)
                    )
                else:
                    stdout.write(
                        u'{} dergisi için dspace import dosyası oluşturulamadı.\n'.format(dergi)
                    )