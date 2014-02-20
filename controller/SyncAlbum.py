import logging
from controller.SyncMedia import SyncMedia
import util.index.Media


class SyncAlbum:
    """Controller 2: uses albums to compare medias."""

    def __init__(self, service_src, service_target, album_src, album_target):
        self.service_src = service_src
        self.service_target = service_target
        self.album_src = album_src
        self.album_target = album_target

    def run(self):
        # load target media elements
        medias_targets_dict = dict((media_target.get_match_name(), media_target) for media_target in self.service_target.Media.Media.fetch_all(self.album_target))

        # check against the index to see if any medias were deleted on source service
        index = util.index.Media.Media(self.service_src, self.album_src)
        index.update()
        for media_src in index.fetch_all_deleted():
            if media_src.get_match_name() in medias_targets_dict:
                logging.getLogger().debug('-- ' + media_src.get_match_name() + ' -- index, will delete media')
                try:
                    medias_targets_dict[media_src.get_match_name()].delete()
                    del medias_targets_dict[media_src.get_match_name()]
                except Exception as e:
                    logging.getLogger().error('delete failed: ' + e.message)
            else:
                logging.getLogger().debug('-- ' + media_src.get_match_name() + ' -- index, will skip media')

        # upload new media
        for media_src in self.service_src.Media.Media.fetch_all(self.album_src):
            if media_src.get_match_name() in medias_targets_dict:
                logging.getLogger().debug('-- ' + media_src.get_match_name() + ' -- sync, will sync existing media')
                media_target = medias_targets_dict[media_src.get_match_name()]
            else:
                logging.getLogger().debug('-- ' + media_src.get_match_name() + ' -- sync, will create new media')
                try:
                    media_target = self.service_target.Media.Media.create(self.album_target, media_src)
                except Exception as e:
                    logging.getLogger().error('create failed: ' + e.message)
                    continue

            try:
                media = SyncMedia(media_src, media_target)
                media.run()
            except Exception as e:
                logging.getLogger().error('media failed: ' + e.message)
