# -*- coding: utf8 -*-
try:
    __instance = unicode
except:
    __instance = str

import gzip
import os
import StringIO
import tempfile
import urllib2

# Some sites blocks default python User-agent
user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
headers = {'User-Agent': user_agent}


def download_file(url, referer=None):
    """ Download file at url and write it to a file, return the path to the file and the url """
    file, path = tempfile.mkstemp()
    file = os.fdopen(file, "w")
    content_type = None
    # Download url
    req = urllib2.Request(url, headers=headers)
    if referer is not None:
        req.add_header('referer', referer)
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError:
        return None, None
    else:
        dat = response.read()
        content_type = response.info().getheader('Content-Type')
        # Check if it is gzipped
        if dat[:2] == '\037\213':
            # Data is gzip encoded, decode it
            compressedstream = StringIO.StringIO(dat)
            gzipper = gzip.GzipFile(fileobj=compressedstream)
            extracted_data = gzipper.read()
            dat = extracted_data

        # Write it to a file
        file.write(dat)
        file.close()
        # return file path
        return path, content_type


class unicode_tr(__instance):
    CHARMAP = {
        "to_upper": {
            u"ı": u"I",
            u"i": u"İ",
            u"ğ": u"Ğ",
            u"ü": u"Ü",
            u"ş": u"Ş",
            u"ö": u"Ö",
            u"ç": u"Ç",
        },
        "to_lower": {
            u"I": u"ı",
            u"İ": u"i",
            u"Ğ": u"ğ",
            u"Ü": u"ü",
            u"Ş": u"ş",
            u"Ö": u"ö",
            u"Ç": u"ç",
        },
        "to_loweer": {
            u"ı": u"i",
            u"ğ": u"g",
            u"ü": u"u",
            u"ş": u"s",
            u"ö": u"o",
            u"ç": u"c",
            u"I": u"i",
            u"İ": u"i",
            u"Ğ": u"g",
            u"Ü": u"u",
            u"Ş": u"s",
            u"Ö": u"o",
            u"Ç": u"c",
        },
    }

    def lower(self):
        for key, value in self.CHARMAP.get("to_lower").items():
            self = self.replace(key, value)
        return self.lower()

    def upper(self):
        for key, value in self.CHARMAP.get("to_upper").items():
            self = self.replace(key, value)
        return self.upper()

    def loweer(self):
        for key, value in self.CHARMAP.get("to_loweer").items():
            self = self.replace(key, value)
        return self.lower()

    def capitalize(self):
        first, rest = self[0], self[1:]
        return unicode_tr(first).upper() + unicode_tr(rest).lower()

    def title(self):
        words = u've ile and with'
        return " ".join(
            map(lambda x: unicode_tr(x).lower() if unicode_tr(x).lower() in words else unicode_tr(x).capitalize(),
                self.split()))
