import os
import urllib
from service.local.Config import Config


class Album:
    """Model: common public api for all albums"""

    @staticmethod
    def fetch_all():
        """walk the directories in directory
        @rtype : list of Album
        """
        entries = []
        for root, dirs, files in os.walk(Config.dir):
            for path in dirs:
                entries.append(Album(path))
        return entries

    @staticmethod
    def create(album_src):
        """
        @type album_src: Album
        @param album_src: source album
        @rtype Album
        """
        path = Config.dir + '/' + urllib.quote(album_src.get_title())
        os.makedirs(path)
        return Album(path)

    def __init__(self, path):
        """
        @type path: string
        @param path: absolute path
        """
        self.path = path

    def get_url(self):
        """
        @rtype : string
        """
        return self.path

    def get_title(self):
        """
        @rtype : string
        """
        return os.path.basename(self.path)

    def get_number_of_media(self):
        """
        @rtype : int
        """
        return len(os.listdir(self.path))

    def get_match_name(self):
        """
        this method is used to match albums
        @rtype : string
        """
        return self.get_title()
