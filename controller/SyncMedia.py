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

        # before comparing ensure, that objects are valid
        if not self.media_src.get_hash():
            self.media_src.save()

        if not self.media_target.get_hash():
            self.media_target.save()

        # check if files are equal
        logging.getLogger().info('checksum ' + self.media_src.get_hash() + ' vs ' + self.media_target.get_hash())

        if self.media_src.get_hash() != self.media_target.get_hash():
            logging.getLogger().debug('checksum is different, but that\'s ok picasa checksum is not trustable')

        if self.media_src.get_size() != self.media_target.get_size():
            logging.getLogger().debug('size in bytes is different')

        if self.media_src.get_date() != self.media_target.get_date():
            logging.getLogger().debug('date is different')

        # then run optional resize of media_src
        if self.media_src.is_resize_necessary():
            self.media_src.resize()

        #todo Do local backups if files are overwritten
        #todo Update meta data (including version?)
        #todo think about etag usage, https://developers.google.com/picasa-web/docs/2.0/developers_guide_protocol
        pass
