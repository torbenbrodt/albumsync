import ConfigParser
import os
import unittest
from controller.List import List
import service.picasa.Config
import util.Bootstrap


class ListTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_picasa_album(self):
        # picasa config
        parser = ConfigParser.ConfigParser()
        parser.read(os.path.join(os.path.expanduser('~'), "albumsync.ini"))
        service.picasa.Config.Config.username = parser.get('credentials', 'username')
        service.picasa.Config.Config.password = parser.get('credentials', 'password')
        if service.picasa.Config.Config.username != 'albumsync.test@gmail.com':
            self.skipTest("The user setup in ~/albumsync.ini does not look like a test user"
                          + ", don't run tests against production system.")
        boot = util.Bootstrap.Bootstrap()
        sync = List(boot.get_service('picasa'), False)
        sync.run()

    def test_picasa_media(self):
        # picasa config
        parser = ConfigParser.ConfigParser()
        parser.read(os.path.join(os.path.expanduser('~'), "albumsync.ini"))
        service.picasa.Config.Config.username = parser.get('credentials', 'username')
        service.picasa.Config.Config.password = parser.get('credentials', 'password')
        if service.picasa.Config.Config.username != 'albumsync.test@gmail.com':
            self.skipTest("The user setup in ~/albumsync.ini does not look like a test user"
                          + ", don't run tests against production system.")
        sync = List(service.picasa, 'http://')
        sync.run()


