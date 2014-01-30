import os
import json
import time
import util.index.Config


class Album:
    """Index Album"""

    def __init__(self, service):
        """
        @param service: AbstractAlbum
        @rtype service:
        """
        self.service = service
        self.path = os.path.join(util.index.Config.Config.dir, self.service.__name__ + '.index')

    def update(self):
        # skip if there is no directory to be indexed
        if not util.index.Config.Config.dir:
            return
        # read media from service
        data_service = dict((album_target.get_match_name(), album_target) for album_target in self.service.Album.Album.fetch_all())
        # read existing index
        data_index = self.fetch_all()
        # check existing data for deletion
        for match_name, album in data_index.items():
            if match_name not in data_service:
                data_index[match_name]['deleted'] = time.time()
            elif 'deleted' in album and album['deleted']:
                data_index[match_name].pop('deleted')

        for match_name, album in data_service.items():
            if match_name not in data_index:
                data_index[album.get_match_name()] = {
                    'indexed': album.get_date()
                }

        fileref = open(self.path, 'w')
        json.dump(data_index, fileref)

    def fetch_all(self):
        data = {}
        if not util.index.Config.Config.dir:
            return data
        try:
            # create dirs
            dirs = os.path.split(self.path)[0]
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            # load json content
            if os.path.exists(self.path):
                fileref = open(self.path, 'r')
                data = json.load(fileref)
        except Exception:
            pass
        return data

    def fetch_all_deleted(self):
        return {k: v for k, v in self.fetch_all().items() if 'deleted' in v and v['deleted']}
