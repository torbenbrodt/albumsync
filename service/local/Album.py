import os
from service.local.Config import Config
from service.abstract.AbstractAlbum import AbstractAlbum
from util.Superconfig import Superconfig


class Album(AbstractAlbum):
    """Model: common public api for all albums"""

    @staticmethod
    def fetch_all():
        """walk the directories
        @rtype : list of Album
        """
        assert Config.dir, "Config.dir cannot be empty"
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
        assert Config.dir, "Config.dir cannot be empty"
        # strip leading slash or dots from beginning for security reason
        title = album_src.get_title().lstrip(os.path.sep + ".")
        path = Config.dir + '/' + title
        path.rstrip(os.path.sep)
        os.makedirs(path)
        return Album(path)

    # noinspection PyMissingConstructor
    def __init__(self, path):
        """
        @type path: string
        @param path: absolute path
        """
        assert Config.dir, "Config.dir cannot be empty"
        if not isinstance(path, unicode):
            path = path.decode('utf-8')
        self.path = path.encode('utf-8').rstrip(os.path.sep)
        self.title = ''

    def get_url(self):
        """
        @rtype : string
        """
        return self.path

    def set_title(self, title):
        self.title = title

    def get_title(self):
        """
        @rtype : string
        """
        if self.title:
            return self.title
        return self.path[len(Config.dir):]

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
        return self.get_title().lower()

    def get_modification_time(self):
        return os.path.getmtime(self.path)

    def get_creation_time(self):
        return self.get_modification_time()

    def delete(self):
        if not Superconfig.allowdelete:
            raise Exception('delete is not allowed')