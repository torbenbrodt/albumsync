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

    def is_hash(self):
        """checksum is not that trustable, picasa does not update hash
        @rtype: bool
        """
        res = self.media_target.get_hash() == self.media_src.get_hash()
        logging.getLogger().debug('is hash' + str(res))
        return res

    def is_filesize_greater_than(self):
        """if source file is bigger than target file
        @rtype: bool
        """
        res = self.media_target.get_filesize() >= self.media_src.get_filesize()
        logging.getLogger().debug('is target greater than ' + str(res))
        return res

    def is_dimensions_greater_than(self):
        """if source file is bigger than target file,
        @rtype: bool
        """
        src_width, src_height = self.media_src.get_dimensions()
        target_width, target_height = self.media_target.get_dimensions()
        res = (src_width * src_height) >= (target_width * target_height)
        logging.getLogger().debug('is target greater than ' + str(res))
        return res

    def is_date_greater_than(self):
        res = self.media_src.get_date() >= self.media_target.get_date()
        logging.getLogger().debug('is date greater than ' + str(res))
        return res

    def is_update_needed(self):
        if not self.is_filesize_greater_than():
            return True
        if not self.is_dimensions_greater_than():
            return True
        if not self.is_date_greater_than():
            return True
        return False

    def run(self):
        # before comparing ensure, that objects are valid
        # todo calls might be better at another place
        if not self.media_src.get_hash():
            self.media_src.save()

        if not self.media_target.get_hash():
            self.media_target.save()

        # then run optional resize of media_src
        if self.media_src.is_resize_necessary():
            self.media_src.resize()

        #todo Do local backups if files are overwritten
        #todo Update meta data (including version?)
        #todo think about etag usage, https://developers.google.com/picasa-web/docs/2.0/developers_guide_protocol
        pass
