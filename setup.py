#!/usr/bin/env python

import os

from setuptools import setup

__version__ = '0.5.3'

# Remove MANIFEST file, since distutils
# doesn't properly update it when
# the contents of directories changes.
if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')

setup(
    name='MAT',
    version=__version__,
    description='Metadata Anonymisation Toolkit',
    long_description='A Metadata Anonymisation Toolkit in Python, using python-hachoir',
    author='jvoisin',
    author_email='julien.voisin@dustri.org',
    platforms='linux',
    license='GPLv2',
    url='https://mat.boum.org',
    packages=['libmat', 'libmat.hachoir_editor', 'libmat.bencode'],
    scripts=['mat', 'mat-gui'],
    test_suite="test",
    data_files=[
        ('share/applications', ['mat.desktop']),
        ('share/mat', ['data/FORMATS', 'data/mat.glade']),
        ('share/pixmaps', ['data/mat.png']),
        ('share/doc/mat', ['README', 'README.security']),
        ('share/man/man1', ['mat.1', 'mat-gui.1']),
        ('share/nautilus-python/extensions', ['nautilus/nautilus-mat.py'])
    ],
    install_requires=['mutagen', 'gi', 'pdfrw', 'hachoir_core', 'hachoir_parser']
)
