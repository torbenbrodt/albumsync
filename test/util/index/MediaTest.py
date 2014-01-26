import os
import tempfile
import unittest
from service.local.Album import Album
import service.local.Config
import service.picasa.Config
import util.index.Media
import util.index.Config
import util.Bootstrap


class MediaTest(unittest.TestCase):

    def setUp(self):
        util.Bootstrap.Bootstrap()
        # index config
        util.index.Config.Config.dir = tempfile.mkdtemp()
        # local config
        service.local.Config.Config.dir = tempfile.mkdtemp()
        # create local album
        os.makedirs(service.local.Config.Config.dir + '/2014/01 Big Data Beers')
        self.album = Album(service.local.Config.Config.dir + '/2014/01 Big Data Beers')

    def test_local_index(self):
        # create local files
        open(service.local.Config.Config.dir + '/2014/01 Big Data Beers/fileA.jpg', 'a').close()
        open(service.local.Config.Config.dir + '/2014/01 Big Data Beers/fileB.jpg', 'a').close()
        open(service.local.Config.Config.dir + '/2014/01 Big Data Beers/fileC.jpg', 'a').close()
        index = util.index.Media.Media(service.local, self.album)
        # check before indexing
        self.assertEquals(0, len(index.fetch_all()))
        self.assertEquals(0, len(index.fetch_all_deleted()))
        # check after indexing
        index.update()
        self.assertEquals(3, len(index.fetch_all()))
        self.assertEquals(0, len(index.fetch_all_deleted()))
        # remove files
        os.remove(service.local.Config.Config.dir + '/2014/01 Big Data Beers/fileA.jpg')
        os.remove(service.local.Config.Config.dir + '/2014/01 Big Data Beers/fileB.jpg')
        # update index again
        index.update()
        self.assertEquals(3, len(index.fetch_all()))
        self.assertEquals(2, len(index.fetch_all_deleted()))
        # now insert one of the files again
        open(service.local.Config.Config.dir + '/2014/01 Big Data Beers/fileA.jpg', 'a').close()
        index.update()
        self.assertEquals(3, len(index.fetch_all()))
        self.assertEquals(1, len(index.fetch_all_deleted()))
