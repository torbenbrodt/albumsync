import util.Image


class SyncMedia:
    """ ... """

    def __init__(self, media_src, media_target):
        self.media_src = media_src
        self.media_target = media_target

    def run(self):
        #todo ask album for restrictions, width + height
        #todo ask if service provides serverside resizing (so any meta data is not lost)
        #todo only resize if album is not public (picasa offers this for free)
        #todo use util.Image.resize
        #todo Do local backups if files are overriden
        #todo Update meta data (including version?)
        #todo think about etag usage, https://developers.google.com/picasa-web/docs/2.0/developers_guide_protocol
        pass
