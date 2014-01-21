class AbstractMedia:
    """Model: common public api for all medias like photos and videos"""

    @staticmethod
    def fetch_all(album):
        """walk the directories
        @type album: Album
        @param album: album
        @rtype : list of AbstractMedia
        """
        raise Exception("method needs to be implemented")

    @staticmethod
    def create(album, media_src):
        """get new instance from existing media
        @type album: Album
        @param album:
        @type media_src: AbstractMedia
        @param media_src:
        """
        raise Exception("method needs to be implemented")

    def __init__(self, album, path):
        """
        @type album: str
        @param album:
        @type path: str
        @param path:
        """
        raise Exception("method needs to be implemented")
    
    def get_url(self):
        """
        @rtype: str
        """
        raise Exception("method needs to be implemented")

    def get_hash(self):
        """
        @rtype: str
        """
        raise Exception("method needs to be implemented")

    def get_date(self):
        """
        returns date
        """
        raise Exception("method needs to be implemented")

    def get_size(self):
        """
        return size in bytes
        @rtype: int
        """
        raise Exception("method needs to be implemented")

    def delete(self):
        """void method
        """
        raise Exception("method needs to be implemented")

    def get_title(self):
        """
        @rtype: str
        """
        raise Exception("method needs to be implemented")

    def get_description(self):
        """
        @rtype: str
        """
        raise Exception("method needs to be implemented")

    def get_mime_type(self):
        """
        @rtype: str
        """
        raise Exception("method needs to be implemented")

    def download(self, path):
        """void method
        """
        raise Exception("method needs to be implemented")

    def get_match_name(self):
        """this method is used to match media
        @rtype: str
        """
        raise Exception("method needs to be implemented")

    def is_resize_necessary(self):
        """
        @rtype: bool
        """
        raise Exception("method needs to be implemented")

    def resize(self):
        """void method
        """
        raise Exception("method needs to be implemented")
