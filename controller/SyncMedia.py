import logging


class SyncMedia:
    """ ... """

    def __init__(self, media_src, media_target):
        """
        @type media_src:
        @param media_src:
        @type media_target:
        @param media_target:
        """
        self.media_src = media_src
        self.media_target = media_target

    def run(self):
        # check if files are equal
        logging.getLogger().info('checksum ' + self.media_src.get_hash() + ' vs ' + self.media_target.get_hash())

        if self.media_src.get_hash() != self.media_target.get_hash():
            pass

        if self.media_src.get_size() != self.media_target.get_size():
            pass

        if self.media_src.get_time() != self.media_target.get_time():
            pass

        # then optional resize of media_src
        if self.media_src.is_resize_necessary():
            self.media_src.resize()
            pass

        #todo Do local backups if files are overwritten
        #todo Update meta data (including version?)
        #todo think about etag usage, https://developers.google.com/picasa-web/docs/2.0/developers_guide_protocol
        pass
