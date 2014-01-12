import unittest
import ConfigParser

from service.picasa.Config import Config
from service.picasa.Album import Album


class AlbumTest(unittest.TestCase):

    def setUp(self):
        parser = ConfigParser.ConfigParser()
        parser.read('/home/tb/albumsync.ini')
        Config.username = parser.get('credentials', 'username')
        Config.password = parser.get('credentials', 'password')

        print "unittests are running for user ", Config.username

    def test_fetchAll(self):
        Album.fetch_all()


