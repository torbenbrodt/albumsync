import os
import tempfile
import unittest
import shutil
import service.local.Config
import service.picasa.Config
import util.index.Album
import util.index.Config
import util.Bootstrap


class AlbumTest(unittest.TestCase):

    def setUp(self):
        util.Bootstrap.Bootstrap()
        # index config
        util.index.Config.Config.dir = tempfile.mkdtemp()
        # local config
        service.local.Config.Config.dir = tempfile.mkdtemp()

    def test_local_index(self):
        # create local fil
        os.makedirs(service.local.Config.Config.dir + '/albumA')
        open(service.local.Config.Config.dir + '/albumA/fileA.jpg', 'a').close()
        os.makedirs(service.local.Config.Config.dir + '/albumB')
        open(service.local.Config.Config.dir + '/albumB/fileB.jpg', 'a').close()
        os.makedirs(service.local.Config.Config.dir + '/albumC')
        open(service.local.Config.Config.dir + '/albumC/fileC.jpg', 'a').close()
        index = util.index.Album.Album(service.local)
        # check before indexing
        self.assertEquals(0, len(index.fetch_all()))
        self.assertEquals(0, len(index.fetch_all_deleted()))
        # check after indexing
        index.sync(True)
        self.assertEquals(3, len(index.fetch_all()))
        self.assertEquals(0, len(index.fetch_all_deleted()))
        # remove folders
        shutil.rmtree(service.local.Config.Config.dir + '/albumA')
        shutil.rmtree(service.local.Config.Config.dir + '/albumB')
        # update index again
        index.sync(True)
        self.assertEquals(3, len(index.fetch_all()))
        self.assertEquals(2, len(index.fetch_all_deleted()))
        # now insert one of the files again
        os.makedirs(service.local.Config.Config.dir + '/albumA')
        open(service.local.Config.Config.dir + '/albumA/fileA.jpg', 'a').close()
        index.sync(True)
        self.assertEquals(3, len(index.fetch_all()))
        self.assertEquals(1, len(index.fetch_all_deleted()))
