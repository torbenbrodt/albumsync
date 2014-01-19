import os
import unittest
import ConfigParser

from service.picasa.Media import Media
from service.picasa.Config import Config
from service.picasa.Album import Album


class MediaTest(unittest.TestCase):

    def setUp(self):
        parser = ConfigParser.ConfigParser()
        parser.read(os.path.join(os.path.expanduser('~'), "albumsync.ini"))
        Config.username = parser.get('credentials', 'username')
        Config.password = parser.get('credentials', 'password')

    def test_fetch_all(self):
        self._addSkip("needs google account for unit testing only")
        album = Album.fetch_all()[1]
        print album.get_title()
        for media in Media.fetch_all(album):
            print media.get_title()

    def test_get_hash(self):
        self._addSkip("needs google account for unit testing only")
        # todo test1 with empty hash
        # todo test2 with hash written back



