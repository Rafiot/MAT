""" Manage which fileformat can be processed
"""

import archive
import audio
import images
import logging
import mat
import misc
import office
import subprocess

STRIPPERS = {
    'application/x-tar': archive.TarStripper,
    'application/x-bzip2': archive.Bzip2Stripper,
    'application/x-gzip': archive.GzipStripper,
    'application/zip': archive.ZipStripper,
    'audio/mpeg': audio.MpegAudioStripper,
    'application/x-bittorrent': misc.TorrentStripper,
    'application/torrent': misc.TorrentStripper,
    'application/opendocument': office.OpenDocumentStripper,
    'application/officeopenxml': office.OpenXmlStripper,
}

logging.basicConfig(level=mat.LOGGING_LEVEL)

# PDF support
pdfSupport = True
try:
    from gi.repository import Poppler
except ImportError:
    logging.info('Unable to import Poppler: no PDF support')
    pdfSupport = False

try:
    import cairo
except ImportError:
    logging.info('Unable to import python-cairo: no PDF support')
    pdfSupport = False

try:
    import pdfrw
except ImportError:
    logging.info('Unable to import python-pdfrw: no PDf support')
    pdfSupport = False

if pdfSupport:
    STRIPPERS['application/x-pdf'] = office.PdfStripper
    STRIPPERS['application/pdf'] = office.PdfStripper


# audio format support with mutagen-python
try:
    import mutagen
    STRIPPERS['audio/x-flac'] = audio.FlacStripper
    STRIPPERS['audio/flac'] = audio.FlacStripper
    STRIPPERS['audio/vorbis'] = audio.OggStripper
    STRIPPERS['audio/ogg'] = audio.OggStripper
    STRIPPERS['audio/mpeg'] = audio.MpegAudioStripper
except ImportError:
    logging.info('Unable to import python-mutagen: limited audio format support')

# exiftool
try:
    subprocess.check_output(['exiftool', '-ver'])
    import exiftool
    STRIPPERS['image/jpeg'] = exiftool.JpegStripper
    STRIPPERS['image/png'] = exiftool.PngStripper
    STRIPPERS['image/tiff'] = exiftool.TiffStripper
except OSError:  # if exiftool is not installed, use hachoir instead
    logging.info('Unable to find exiftool: limited images support')
    STRIPPERS['image/jpeg'] = images.JpegStripper
    STRIPPERS['image/png'] = images.PngStripper
