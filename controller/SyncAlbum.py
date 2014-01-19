import logging
from controller.SyncMedia import SyncMedia


class SyncAlbum:
    """Controller 2: uses albums to compare medias."""

    def __init__(self, service_src, service_target, album_src, album_target):
        self.service_src = service_src
        self.service_target = service_target
        self.album_src = album_src
        self.album_target = album_target

    def run(self):
        medias_targets_dict = dict((media_target.get_match_name(), media_target) for media_target in self.service_target.Media.Media.fetch_all(self.album_target))
        for media_src in self.service_src.Media.Media.fetch_all(self.album_src):
            if medias_targets_dict.has_key(media_src.get_match_name()):
                logging.getLogger().info(media_src.get_match_name() + ', media match: yes')
                media_target = medias_targets_dict[media_src.get_match_name()]
            else:
                logging.getLogger().info(media_src.get_match_name() + ', media match: no')
                media_target = self.service_target.Media.Media.create(self.album_target, media_src)

            media = SyncMedia(media_src, media_target)
            media.run()
