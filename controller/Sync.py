import logging
from controller.SyncAlbum import SyncAlbum
import util.index.Album
import util.Bootstrap
import util.Superconfig


class Sync:
    """Controller 1: uses services to compare albums."""

    def __init__(self, service_src, service_target, album_src):
        assert service_src, "when using sync action, src cannot be empty"
        assert service_target, "when using sync action, target cannot be empty"
        boot = util.Bootstrap.Bootstrap()
        self.service_src = boot.get_service(service_src)
        self.service_target = boot.get_service(service_target)
        self.album_str = album_src

    def _get_albums(self, service):
        if (service == self.service_src and util.Superconfig.Superconfig.from_index_src) or (
                self.service_target == service and util.Superconfig.Superconfig.from_index_target):
            index = util.index.Album.Album(service)
            index.update()
            return index.fetch_all_as_album()
        else:
            return service.Album.Album.fetch_all()

    def run(self):
        albums_targets_dict = dict((album_target.get_match_name(), album_target) for album_target in
                                   self._get_albums(self.service_target))

        if self.album_str:
            boot = util.Bootstrap.Bootstrap()
            album_src_list = [boot.get_album(self.service_src, self.album_str)]
        else:
            # check against the index to see if any albums were deleted on source service
            index = util.index.Album.Album(self.service_src)
            index.update()
            for album_src in index.fetch_all_deleted():
                if album_src.get_match_name() in albums_targets_dict:
                    logging.getLogger().debug('-- ' + album_src.get_match_name() + ' -- index, will delete album')
                    albums_targets_dict[album_src.get_match_name()].delete()
                    # remove from dictionary
                    del albums_targets_dict[album_src.get_match_name()]
                else:
                    logging.getLogger().debug('-- ' + album_src.get_match_name() + ' -- index, will skip album')
            album_src_list = self._get_albums(self.service_src)
        self.sync_service(album_src_list, albums_targets_dict)

    def sync_service(self, album_src_list, albums_targets_dict):
        for album_src in album_src_list:
            if album_src.get_match_name() in albums_targets_dict:
                logging.getLogger().debug('-- ' + album_src.get_match_name() + ' -- sync, will sync existing album')
                album_target = albums_targets_dict[album_src.get_match_name()]
            else:
                logging.getLogger().debug('-- ' + album_src.get_match_name() + ' -- sync, will create new album')
                album_target = self.service_target.Album.Album.create(album_src)

            album = SyncAlbum(self.service_src, self.service_target, album_src, album_target)
            album.run()
