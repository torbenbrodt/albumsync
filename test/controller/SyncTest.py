import os
import tempfile
import unittest
import ConfigParser
from controller.Sync import Sync
import service.local.Config
import service.picasa.Config


class SyncTest(unittest.TestCase):

    def setUp(self):
        # local config
        service.local.Config.Config.dir = tempfile.mkdtemp()
        # picasa config
        parser = ConfigParser.ConfigParser()
        parser.read(os.path.join(os.path.expanduser('~'), "albumsync.ini"))
        service.picasa.Config.Config.username = parser.get('credentials', 'username')
        service.picasa.Config.Config.password = parser.get('credentials', 'password')

    def test_run_from_picasa_to_local(self):
        # todo, disable imports and load automatically from Sync class
        # module = __import__('service.local', fromlist=['Album'])
        # getattr(module, 'Album')
        import service.local.Album
        import service.picasa.Album

        sync = Sync(service.picasa, service.local)
        sync.run()


