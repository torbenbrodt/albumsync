import os
import unittest
import ConfigParser

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


