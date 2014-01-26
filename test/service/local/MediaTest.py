import tempfile
import unittest
import os
from service.local.Config import Config
from service.local.Album import Album
from service.local.Media import Media
import service.local.Media
import util.Bootstrap


class MediaTest(unittest.TestCase):

    def setUp(self):
        util.Bootstrap.Bootstrap()
        self.dir = tempfile.mkdtemp()
        Config.dir = self.dir

    def test_fetchAll(self):
        # create directory
        os.makedirs(self.dir + '/2014')
        album = Album(self.dir + '/2014')
        # create some media
        open(self.dir + '/2014/fileA.jpg', 'a').close()
        open(self.dir + '/2014/fileB.jpg', 'a').close()
        open(self.dir + '/2014/fileC.jpg', 'a').close()
        # find those directories
        self.assertIs(3, len(service.local.Media.Media.fetch_all(album)))
        # check contents
        x = map(lambda media: media.get_title(), service.local.Media.Media.fetch_all(album))
        x.sort()
        self.assertEquals(['fileA.jpg', 'fileB.jpg', 'fileC.jpg'], x)

    def test_create(self):
        # create source
        os.makedirs(self.dir + '/a')
        album_src = Album(self.dir + '/a')
        open(self.dir + '/a/fileA.jpg', 'a').close()
        media_src = Media(album_src, self.dir + '/a/fileA.jpg')
        # create target
        os.makedirs(self.dir + '/b')
        album_target = Album(self.dir + '/b')
        # should be empty
        self.assertIs(0, len(service.local.Media.Media.fetch_all(album_target)))
        Media.create(album_target, media_src)
        self.assertIs(1, len(service.local.Media.Media.fetch_all(album_target)))

    def test_get_title(self):
        # create source
        os.makedirs(self.dir + '/a')
        album = Album(self.dir + '/a')
        open(self.dir + '/a/fileA.jpg', 'a').close()
        media = Media(album, self.dir + '/a/fileA.jpg')
        self.assertEquals("fileA.jpg", media.get_title())
        open(self.dir + '/a/fileA with spaces.jpg', 'a').close()
        media = Media(album, self.dir + '/a/fileA with spaces.jpg')
        self.assertEquals("fileA with spaces.jpg", media.get_title())


