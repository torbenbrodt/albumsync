import os
import tempfile
import unittest
import ConfigParser
from controller.Sync import Sync
import service.local.Config
import service.picasa.Config
import util.Bootstrap


class SyncTest(unittest.TestCase):

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
        if False and service.picasa.Config.Config.username != 'albumsync.test@gmail.com':
            self.skipTest("The user setup in ~/albumsync.ini does not look like a test user"
                          + ", don't run tests against production system.")
        # create some remote albums
        sync = Sync('picasa', 'local', 'http://picasaweb.google.com/data/feed/api/user/117639953293800513895/albumid/5903155118841778945?kind=photo')
        sync.run()
