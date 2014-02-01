import logging
from controller.SyncAlbum import SyncAlbum
import util.index.Album


class Sync:
    """Controller 1: uses services to compare albums."""

    def __init__(self, service_src, service_target):
        assert service_src, "when using sync action, src cannot be empty"
        assert service_target, "when using sync action, target cannot be empty"
        self.service_src = service_src
        self.service_target = service_target

    def run(self):
        albums_targets_dict = dict((album_target.get_match_name(), album_target) for album_target in self.service_target.Album.Album.fetch_all())

        # check against the index to see if any albums were deleted on source service
        index = util.index.Album.Album(self.service_src)
        index.update()
        for album_src in index.fetch_all_deleted():
            if album_src.get_match_name() in albums_targets_dict:
                logging.getLogger().info(album_src.get_match_name() + ', delete album match: yes')
                media_target = albums_targets_dict[album_src.get_match_name()]
                media_target.delete()
            else:
                logging.getLogger().info(album_src.get_match_name() + ', delete album match: no')

        # upload new media
        for album_src in self.service_src.Album.Album.fetch_all():
            if album_src.get_match_name() in albums_targets_dict:
                logging.getLogger().info(album_src.get_match_name() + ', album match: yes')
                album_target = albums_targets_dict[album_src.get_match_name()]
            else:
                logging.getLogger().info(album_src.get_match_name() + ', album match: no')
                album_target = self.service_target.Album.Album.create(album_src)

            album = SyncAlbum(self.service_src, self.service_target, album_src, album_target)
            album.run()
