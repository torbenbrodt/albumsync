import os
from util.index import Config


class Album:
    """Index Album"""

    def flush(self):
        """delete index file
        """
        pass

    def fetch_delete(self):
        pass

    def __init__(self, service):
        """access config.dir/index/{service}.index
        @rtype : list of Album
        """
        self.entries = []

        for root, dirs, files in os.walk(Config.dir):
            for path in dirs:
                album_path = os.path.join(root, path)
                album_root, album_dirs, album_files = os.walk(album_path).next()
                # only find directories which include files
                if len(album_files):
                    entries.append(Album(album_path))