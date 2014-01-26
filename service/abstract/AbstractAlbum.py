from abc import ABCMeta, abstractmethod


class AbstractAlbum:
    __metaclass__  = ABCMeta
    """Model: common public api for all albums"""

    @staticmethod
    @abstractmethod
    def fetch_all():
        """
        @rtype list of Album
        @raise Exception:
        """
        pass

    @staticmethod
    @abstractmethod
    def create(album_src):
        """
        @type album_src: AbstractAlbum
        @param album_src: source album
        @rtype Album
        """
        pass

    @abstractmethod
    def __init__(self, path):
        """
        @type path: str
        @param path: absolute path
        """
        pass

    @abstractmethod
    def get_url(self):
        """
        @rtype : str
        """
        pass

    @abstractmethod
    def get_title(self):
        """
        @rtype : str
        """
        pass

    @abstractmethod
    def get_number_of_media(self):
        """
        @rtype : int
        """
        pass

    @abstractmethod
    def get_match_name(self):
        """
        this method is used to match albums
        @rtype : str
        """
        pass
