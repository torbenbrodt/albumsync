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

    def test_fetchAll(self):
        album = Album.fetch_all()[0]
        for media in Media.fetch_all(album):
            print media


