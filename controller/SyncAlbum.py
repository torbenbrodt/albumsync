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
                logging.getLogger().info(media_src.get_match_name() + ', delete media match: yes')
                media_target = medias_targets_dict[media_src.get_match_name()]
                media_target.delete()
            else:
                logging.getLogger().info(media_src.get_match_name() + ', delete media match: no')

        # upload new media
        for media_src in self.service_src.Media.Media.fetch_all(self.album_src):
            if media_src.get_match_name() in medias_targets_dict:
                logging.getLogger().info(media_src.get_match_name() + ', update media match: yes')
                media_target = medias_targets_dict[media_src.get_match_name()]
            else:
                logging.getLogger().info(media_src.get_match_name() + ', update media match: no')
                media_target = self.service_target.Media.Media.create(self.album_target, media_src)

            media = SyncMedia(media_src, media_target)
            media.run()
