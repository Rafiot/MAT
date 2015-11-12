#!/usr/bin/env python
# -*- coding: utf-8 -*

"""
    Class for the testing suite :
    - get the list of all test files
    - create a copy of them on start
    - remove the copy on end
"""

import shutil
import os
import glob
import sys
import tempfile
import unittest

VERBOSITY = 15

cur_dir = os.path.dirname(os.path.realpath(__file__))

clean = glob.glob(os.path.join(cur_dir, 'clean*'))
clean.sort()
dirty = glob.glob(os.path.join(cur_dir, 'dirty*'))
dirty.sort()

FILE_LIST = zip(clean, dirty)

try:  # PDF render processing
    import cairo
    import gi
    from gi.repository import Poppler
    import pdfrw
except ImportError:
    FILE_LIST.remove((os.path.join(cur_dir, 'clean é.pdf'), os.path.join(cur_dir, 'dirty é.pdf')))

try:  # python-mutagen : audio file format
    import mutagen
except ImportError:
    FILE_LIST.remove((os.path.join(cur_dir, 'clean é.ogg'), os.path.join(cur_dir, 'dirty é.ogg')))
    FILE_LIST.remove((os.path.join(cur_dir, 'clean é.mp3'), os.path.join(cur_dir, 'dirty é.mp3')))
    FILE_LIST.remove((os.path.join(cur_dir, 'clean é.flac'), os.path.join(cur_dir, 'dirty é.flac')))


class MATTest(unittest.TestCase):
    """
        Parent class of all test-functions
    """

    def setUp(self):
        """
            Create working copy of the clean and the dirty file in the TMP dir
        """
        self.file_list = []
        self.cur_dir = cur_dir
        self.tmpdir = tempfile.mkdtemp()

        for clean_file, dirty_file in FILE_LIST:
            clean_dir = os.path.join(self.tmpdir, os.path.basename(clean_file))
            dirty_dir = os.path.join(self.tmpdir, os.path.basename(dirty_file))
            shutil.copy2(clean_file, clean_dir)
            shutil.copy2(dirty_file, dirty_dir)
            self.file_list.append((clean_dir, dirty_dir))

    def tearDown(self):
        """
            Remove the tmp folder
        """
        for root, dirs, files in os.walk(self.tmpdir):
            for d in dirs + files:
                os.chmod(os.path.join(root, d), 0o777)
        shutil.rmtree(self.tmpdir)


if __name__ == '__main__':
    import clitest
    import libtest

    SUITE = unittest.TestSuite()
    SUITE.addTests(clitest.get_tests())
    SUITE.addTests(libtest.get_tests())

    ret = unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE).wasSuccessful()
    sys.exit(ret is False)
