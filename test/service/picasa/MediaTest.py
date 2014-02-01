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
        if Config.username != 'albumsync.test@gmail.com':
            self.skipTest("The user setup in ~/albumsync.ini does not look like a test user"
                          + ", don't run tests against production system.")

    def test_fetch_all(self):
        album = Album.fetch_all()[1]
        print album.get_title()
        for media in Media.fetch_all(album):
            print media.get_title()

    def test_get_hash(self):
        self.skipTest("needs implementation")
        pass



