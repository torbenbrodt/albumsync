import logging
from controller.SyncMedia import SyncMedia
import service.index.Album
import service.index.Media


class SyncAlbum:
    """Controller 2: uses albums to compare medias."""

    def __init__(self, service_src, service_target, album_src, album_target):
        self.service_src = service_src
        self.service_target = service_target
        self.album_src = album_src
        self.album_target = album_target

    def run(self):
        #todo load old index of album_src
        medias_srcs_dict = dict((media_src.get_match_name(), media_src) for media_src in self.service_src.Media.Media.fetch_all(self.album_src))
        for media_index in service.index.Media.Media.fetch_all(self.album_src):
            if media_index.get_match_name() in medias_srcs_dict:
                #todo delete medias of album_src, which was deleted
                #todo build new index of album_src
                pass

        medias_targets_dict = dict((media_target.get_match_name(), media_target) for media_target in self.service_target.Media.Media.fetch_all(self.album_target))
        for media_src in self.service_src.Media.Media.fetch_all(self.album_src):
            if media_src.get_match_name() in medias_targets_dict:
                logging.getLogger().info(media_src.get_match_name() + ', media match: yes')
                media_target = medias_targets_dict[media_src.get_match_name()]
            else:
                logging.getLogger().info(media_src.get_match_name() + ', media match: no')
                media_target = self.service_target.Media.Media.create(self.album_target, media_src)

            media = SyncMedia(media_src, media_target)
            media.run()
