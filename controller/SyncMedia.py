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

    def _cmp_hash(self):
        """
        checksum is not that trustable, picasa does not update hash automatically
        if hash is the different, then the target may want an update
        if hash is the same, then there is no update needed
        @return: >1 if target item should get an update
        @rtype: int
        """
        return 0 if self.media_target.get_hash() == self.media_src.get_hash() else 1

    def _cmp_filesize(self):
        """
        if source file is greater than target file, then the target may want an update
        if target file is greater than source file, then there is no update needed
        @return: >1 if target item should get an update
        @rtype: int
        """
        return int.__cmp__(self.media_src.get_filesize(), self.media_target.get_filesize())

    def _cmp_dimensions(self):
        """
        if source file is greater than target file, then the target may want an update
        if target file is greater than source file, then there is no update needed
        @return: >1 if target item should get an update
        @rtype: int
        """
        src_width, src_height = self.media_src.get_dimensions()
        target_width, target_height = self.media_target.get_dimensions()
        return int.__cmp__(src_width * src_height, target_width * target_height)

    def _cmp_creation_time(self):
        """
        if source file is newer than target file, then the target may want an update
        if target file is newer than source file, then there is no update needed
        @return: >1 if target item should get an update
        @rtype: int
        """
        # we parse to int, to only compare second, rather than milliseconds
        return int.__cmp__(int(self.media_src.get_creation_time()), int(self.media_target.get_creation_time()))

    def _cmp_modification_time(self):
        """
        if source file is newer than target file, then the target may want an update
        if target file is newer than source file, then there is no update needed
        @return: >1 if target item should get an update
        @rtype: int
        """
        # we parse to int, to only compare second, rather than milliseconds
        return int.__cmp__(int(self.media_src.get_modification_time()), int(self.media_target.get_modification_time()))

    def get_score(self):
        score = 0

        # if modification of local data is newer than picasa, this is trustable
        # if modification of picasa data is newer than
        # modification of picasa can be date of upload
        if self._cmp_modification_time() > 0:
            if self.media_src.get_creation_time() == self.media_target.get_modification_time():
                logging.getLogger().debug('modification time of source is newer, but '
                                          'but creation time of source item equals modification time of target'
                                          'and this is good')
            else:
                logging.getLogger().debug('modification time of source is newer')
                score += 1

            if self._cmp_dimensions() < 0:
                logging.getLogger().debug('dimensions are smaller, skip')
                score -= 1

        if self._cmp_creation_time() != 0 and self._cmp_hash() != 0:
            logging.getLogger().debug('creation time and hash are different, this is probably not the same image')
            score = 0

        # todo comparison currently is not safe, changes in picasa are not properly detected
        return 0

    def run(self):
        # before comparing ensure, that objects are valid
        changed = self.media_target.validate()
        score = self.get_score()
        if score > 0:
            self.media_target.update_blob(self.media_src)
        if score > 0 or changed:
            logging.getLogger().warn('target img will be updated, resulting score is ' + str(score))
            self.media_target.save()
