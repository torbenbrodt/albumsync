import tempfile
import unittest
import os
from service.local.Config import Config
from service.local.Album import Album


class AlbumTest(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        Config.dir = self.dir

    def test_fetchAll(self):
        # create some directories
        os.makedirs(self.dir + '/a')
        os.makedirs(self.dir + '/b')
        os.makedirs(self.dir + '/c')
        # find those directories
        albums = Album.fetch_all()
        self.assertIs(3, len(albums))
        # create some files, which should not be found
        open(self.dir + 'fileA', 'a').close()
        # find those directories
        self.assertIs(3, len(Album.fetch_all()))
        # check contents
        x = map(lambda album: album.get_title(), Album.fetch_all())
        x.sort()
        self.assertEquals(['a', 'b', 'c'], x)

    def test_create(self):
        album_src = Album(self.dir + '/a')
        self.assertIs(0, len(Album.fetch_all()))
        Album.create(album_src)
        self.assertIs(1, len(Album.fetch_all()))

    def test_get_title(self):
        album = Album(self.dir + '/a')
        self.assertEquals("a", album.get_title())
        album = Album(self.dir + '/a with spaces')
        self.assertEquals("a with spaces", album.get_title())


