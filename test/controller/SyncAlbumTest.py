import os
import tempfile
import unittest
import ConfigParser
from controller.SyncAlbum import SyncAlbum
import service.local.Config
import service.picasa.Config
import util.Bootstrap


class SyncAlbumTest(unittest.TestCase):

    def setUp(self):
        util.Bootstrap.Bootstrap()
        # local config
        service.local.Config.Config.dir = tempfile.mkdtemp()
        # create some local folders, level 1
        os.makedirs(service.local.Config.Config.dir + '/toplevel')
        open(service.local.Config.Config.dir + '/toplevel/fileA.jpg', 'a').close()
        os.makedirs(service.local.Config.Config.dir + '/2014/01 Big Data Beers')
        open(service.local.Config.Config.dir + '/2014/01 Big Data Beers/fileB.jpg', 'a').close()

    def test_run_from_picasa_to_local(self):
        # picasa config
        parser = ConfigParser.ConfigParser()
        parser.read(os.path.join(os.path.expanduser('~'), "albumsync.ini"))
        service.picasa.Config.Config.username = parser.get('credentials', 'username')
        service.picasa.Config.Config.password = parser.get('credentials', 'password')
        if service.picasa.Config.Config.username != 'albumsync.test@gmail.com':
            self.skipTest("The user setup in ~/albumsync.ini does not look like a test user"
                          + ", don't run tests against production system.")
        # create some remote albums
        sync = SyncAlbum(service.picasa, service.local, self.album_src, self.album_target)
        sync.run()


