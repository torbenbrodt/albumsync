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

    def _is_hash_different(self):
        """
        checksum is not that trustable, picasa does not update hash automatically
        if hash is the different, then the target may want an update
        if hash is the same, then there is no update needed
        @return: true if target item should get an update
        @rtype: bool
        """
        res = self.media_target.get_hash() != self.media_src.get_hash()
        if res:
            logging.getLogger().debug('UPDATE hash: is different %s vs %s' %
                                      (self.media_target.get_hash(), self.media_src.get_hash()))
        return res

    def _is_filesize_greater_than(self):
        """
        if source file is greater than target file, then the target may want an update
        if target file is greater than source file, then there is no update needed
        @return: true if target item should get an update
        @rtype: bool
        """
        res = self.media_src.get_filesize() > self.media_target.get_filesize()
        if res:
            logging.getLogger().debug('UPDATE filesize: %s is greater than %s' %
                                      (self.media_src.get_filesize(), self.media_target.get_filesize()))
        return res

    def _is_dimensions_greater_than(self):
        """
        if source file is greater than target file, then the target may want an update
        if target file is greater than source file, then there is no update needed
        @return: true if target item should get an update
        @rtype: bool
        """
        src_width, src_height = self.media_src.get_dimensions()
        target_width, target_height = self.media_target.get_dimensions()
        res = (src_width * src_height) > (target_width * target_height)
        if res:
            logging.getLogger().debug('UPDATE dimensions: %s is greater than %s' %
                                      (self.media_src.get_dimensions(), self.media_target.get_dimensions()))
        return res

    def _is_creation_time_greater_than(self):
        """
        if source file is newer than target file, then the target may want an update
        if target file is newer than source file, then there is no update needed
        @return: true if target item should get an update
        @rtype: bool
        """
        res = self.media_src.get_creation_time() > self.media_target.get_creation_time()
        if res:
            logging.getLogger().debug('UPDATE creation time: %s is greater than %s' %
                                      (self.media_src.get_creation_time(), self.media_target.get_creation_time()))
        return res

    def _is_modification_time_greater_than(self):
        """
        if source file is newer than target file, then the target may want an update
        if target file is newer than source file, then there is no update needed
        @return: true if target item should get an update
        @rtype: bool
        """
        res = self.media_src.get_modification_time() > self.media_target.get_modification_time()
        if res:
            logging.getLogger().debug('UPDATE modification time: %s is greater than %s' %
                                      (self.media_src.get_modification_time(), self.media_target.get_modification_time()))
        return res

    def get_score(self):
        score = 0
        if self._is_hash_different():
            score += 1
        if self._is_creation_time_greater_than():
            score += 2
        else:
            # its a good sign if modification time wants to update
            score -= 2
        # modification time possible due to crc update
        if self._is_modification_time_greater_than():
            score += 1
        else:
            # its a good sign if modification time wants to update
            score -= 1
        if self._is_filesize_greater_than():
            score += 1
        if self._is_dimensions_greater_than():
            score += 1
        return score

    def run(self):
        # before comparing ensure, that objects are valid
        self.media_src.validate()
        self.media_target.validate()

        score = self.get_score()
        if score > 0:
            logging.getLogger().info('target img is outdated')
            self.media_target.update_blob(self.media_src)
        if self.media_target.is_resize_necessary():
            logging.getLogger().info('target img is too big')
            if self.media_target.resize():
                score = 1
        if score > 0:
            logging.getLogger().warn('target img will be updated, resulting score is ' + str(score))
            self.media_target.save()
