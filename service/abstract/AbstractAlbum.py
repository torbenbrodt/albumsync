class AbstractAlbum:
    """Model: common public api for all albums"""

    @staticmethod
    def fetch_all():
        """
        @rtype list of Album
        @raise Exception:
        """
        raise Exception("method needs to be implemented")

    @staticmethod
    def create(album_src):
        """
        @type album_src: AbstractAlbum
        @param album_src: source album
        @rtype Album
        """
        raise Exception("method needs to be implemented")

    def __init__(self, path):
        """
        @type path: str
        @param path: absolute path
        """
        raise Exception("method needs to be implemented")

    def get_url(self):
        """
        @rtype : str
        """
        raise Exception("method needs to be implemented")

    def get_title(self):
        """
        @rtype : str
        """
        raise Exception("method needs to be implemented")

    def get_number_of_media(self):
        """
        @rtype : int
        """
        raise Exception("method needs to be implemented")

    def get_match_name(self):
        """
        this method is used to match albums
        @rtype : str
        """
        raise Exception("method needs to be implemented")
