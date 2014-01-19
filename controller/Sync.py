import logging
from controller.SyncAlbum import SyncAlbum

# todo, disable imports and load automatically from Sync class
# module = __import__('service.local', fromlist=['Album'])
# getattr(module, 'Album')
import service.picasa.Album
import service.local.Album
import service.picasa.Media
import service.local.Media


class Sync:
    """Controller 1: uses services to compare albums."""

    def __init__(self, service_src, service_target):
        self.service_src = service_src
        self.service_target = service_target

    def run(self):
        albums_targets_dict = dict((album_target.get_match_name(), album_target) for album_target in self.service_target.Album.Album.fetch_all())
        for album_src in self.service_src.Album.Album.fetch_all():
            if albums_targets_dict.has_key(album_src.get_match_name()):
                logging.getLogger().info(album_src.get_match_name() + ', album match: yes')
                album_target = albums_targets_dict[album_src.get_match_name()]
            else:
                logging.getLogger().info(album_src.get_match_name() + ', album match: no')
                album_target = self.service_target.Album.Album.create(album_src)

            album = SyncAlbum(self.service_src, self.service_target, album_src, album_target)
            album.run()
