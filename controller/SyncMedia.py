import util.Image


class SyncMedia:
    """ ... """

    def __init__(self, media_src, media_target):
        self.media_src = media_src
        self.media_target = media_target

    def run(self):

        # check if files are equal
        if self.media_src.get_hash() == self.media_target.get_hash():
            pass

        #todo check if file was updated

        # then optional resize of media_src
        if self.media_src.is_resize_necessary():
            self.media_src.resize()
            pass

        #todo Do local backups if files are overwritten
        #todo Update meta data (including version?)
        #todo think about etag usage, https://developers.google.com/picasa-web/docs/2.0/developers_guide_protocol
        pass
