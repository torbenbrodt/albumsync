import os
import tempfile
import unittest
import shutil
from controller.SyncMedia import SyncMedia
from service.local.Album import Album
from service.local.Media import Media
import service.local.Config
import service.picasa.Config
import util.Bootstrap


class SyncMediaTest(unittest.TestCase):
    def setUp(self):
        util.Bootstrap.Bootstrap()
        # local config
        service.local.Config.Config.dir = tempfile.mkdtemp()

    def test_run_from_local_to_local_files_same(self):
        # create local albums
        os.makedirs(service.local.Config.Config.dir + '/A')
        album_src = Album(service.local.Config.Config.dir + '/A')
        os.makedirs(service.local.Config.Config.dir + '/B')
        album_target = Album(service.local.Config.Config.dir + '/B')
        # get real images
        path_src = service.local.Config.Config.dir + '/A/openartproject_city_limits.jpg'
        path_target = service.local.Config.Config.dir + '/B/openartproject_city_limits.jpg'
        path_test = os.path.dirname(os.path.abspath(__file__)) + '/../data/openartproject_city_limits.jpg'
        shutil.copyfile(path_test, path_src)
        shutil.copyfile(path_test, path_target)
        media_src = Media(album_src, path_src)
        media_target = Media(album_target, path_target)
        sync = SyncMedia(media_src, media_target)
        # compare
        self.assertTrue(sync.is_hash())
        self.assertTrue(sync.is_filesize_greater_than())
        self.assertTrue(sync.is_modification_time_greater_than())
        self.assertTrue(sync.is_dimensions_greater_than())
        self.assertFalse(sync.is_update_needed())
        # action
        self.run()

    def test_run_from_local_to_picasa_files_same(self):
        pass
