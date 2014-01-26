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

    def test_files_same(self):
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
        # compare
        sync = SyncMedia(media_src, media_target)
        sync.run()
