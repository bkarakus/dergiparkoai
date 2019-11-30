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
    # Download url
    req = urllib2.Request(url, headers=headers)
    if referer is not None:
        req.add_header('referer', referer)
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError:
        return None
    else:
        dat = response.read()
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
        return path
