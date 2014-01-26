import os
import urllib
from service.local.Config import Config
from service.abstract.AbstractAlbum import AbstractAlbum


class Album(AbstractAlbum):
    """Model: common public api for all albums"""

    @staticmethod
    def fetch_all():
        """walk the directories
        @rtype : list of Album
        """
        entries = []
        for root, dirs, files in os.walk(Config.dir):
            for path in dirs:
                album_path = os.path.join(root, path)
                album_root, album_dirs, album_files = os.walk(album_path).next()
                # only find directories which include files
                if len(album_files):
                    entries.append(Album(album_path))
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
        return self.path[len(Config.dir) + 1:]

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
