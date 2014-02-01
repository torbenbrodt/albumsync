import tempfile
import unittest
import os
from service.local.Config import Config
from service.local.Album import Album


class AlbumTest(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        Config.dir = self.dir

    def test_fetch_all(self):
        # create some directories
        os.makedirs(self.dir + '/2013/a')
        os.makedirs(self.dir + '/2013/b')
        os.makedirs(self.dir + '/toplevel')
        # those directories have no files, so result is empty
        albums = Album.fetch_all()
        self.assertIs(0, len(albums))
        # create some files, which make an album an album
        open(self.dir + '/2013/a/fileA.jpg', 'a').close()
        open(self.dir + '/2013/b/fileB.jpg', 'a').close()
        open(self.dir + '/toplevel/top1.jpg', 'a').close()
        # find those directories
        self.assertIs(3, len(Album.fetch_all()))
        # check contents
        x = map(lambda album: album.get_title(), Album.fetch_all())
        x.sort()
        self.assertEquals(['2013/a', '2013/b', 'toplevel'], x)

    def test_create(self):
        album_src = Album(self.dir + '/a')
        self.assertIs(0, len(Album.fetch_all()))
        Album.create(album_src)
        open(self.dir + '/a/fileA.jpg', 'a').close()
        self.assertIs(1, len(Album.fetch_all()))

    def test_get_title(self):
        album = Album(self.dir + '/a')
        self.assertEquals("a", album.get_title())
        album = Album(self.dir + '/a with spaces')
        self.assertEquals("a with spaces", album.get_title())


