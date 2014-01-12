import os
import tempfile
import unittest
import ConfigParser
import service.local.Album

from service.picasa.Config import Config
from service.picasa.Album import Album


class AlbumTest(unittest.TestCase):

    def setUp(self):
        parser = ConfigParser.ConfigParser()
        parser.read(os.path.join(os.path.expanduser('~'), "albumsync.ini"))
        Config.username = parser.get('credentials', 'username')
        Config.password = parser.get('credentials', 'password')

    def test_fetchAll(self):
        for album in Album.fetch_all():
            print "\"", album.get_title(), "\" has", album.get_number_of_media(), "entries"

    def test_create(self):
        self._addSkip("don't want to mess up during testing")
        length_old = len(Album.fetch_all())
        album_src = service.local.Album.Album(tempfile.mkdtemp() + '/a')
        album = Album.create(album_src)
        self.assertIs(length_old + 1, len(Album.fetch_all()))
        self.assertIsInstance(album, "Album")

    def test_delete(self):
        self._addSkip("don't want to do dangerous stuff during testing, needs google account for unit testing only")
        length_old = len(Album.fetch_all())
        album_src = service.local.Album.Album(tempfile.mkdtemp() + '/a')
        album = Album.create(album_src)
        self.assertIs(length_old + 1, len(Album.fetch_all()))
        album.delete()
        self.assertIs(length_old, len(Album.fetch_all()))


