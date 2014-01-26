from abc import ABCMeta, abstractmethod


class AbstractMedia:
    __metaclass__  = ABCMeta
    """Model: common public api for all medias like photos and videos"""

    @staticmethod
    @abstractmethod
    def fetch_all(album):
        """walk the directories
        @type album: Album
        @param album: album
        @rtype : list of AbstractMedia
        """
        pass

    @staticmethod
    @abstractmethod
    def create(album, media_src):
        """get new instance from existing media
        @type album: Album
        @param album:
        @type media_src: AbstractMedia
        @param media_src:
        """
        pass

    @abstractmethod
    def __init__(self, album, path):
        """
        @type album: str
        @param album:
        @type path: str
        @param path:
        """
        pass
    
    @abstractmethod
    def get_url(self):
        """
        @rtype: str
        """
        pass

    @abstractmethod
    def get_hash(self):
        """
        @rtype: str
        """
        pass

    @abstractmethod
    def get_date(self):
        """
        returns date
        """
        pass

    @abstractmethod
    def get_size(self):
        """
        return size in bytes
        @rtype: int
        """
        pass

    @abstractmethod
    def delete(self):
        """void method
        """
        pass

    @abstractmethod
    def get_title(self):
        """
        @rtype: str
        """
        pass

    @abstractmethod
    def get_description(self):
        """
        @rtype: str
        """
        pass

    @abstractmethod
    def get_mime_type(self):
        """
        @rtype: str
        """
        pass

    @abstractmethod
    def download(self, path):
        """void method
        """
        pass

    @abstractmethod
    def get_match_name(self):
        """this method is used to match media
        @rtype: str
        """
        pass

    @abstractmethod
    def is_resize_necessary(self):
        """
        @rtype: bool
        """
        pass

    @abstractmethod
    def resize(self):
        """void method
        """
        pass
