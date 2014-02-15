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

        # read existing index
        index = self.fetch()

        # todo implement ttl
        # check ttl
        if not util.index.Config.Config.ttl or index.last_update - time > util.index.Config.Config.ttl:
            return

        index_entry = index['entry']

        # read media from service
        data_service = dict((album_target.get_match_name(), album_target) for album_target in self.service.Album.Album.fetch_all())

        # check existing data for deletion
        for match_name, album in index_entry.items():
            if match_name not in data_service:
                index_entry[match_name]['deleted'] = time.time()
            elif 'deleted' in album and album['deleted']:
                index_entry[match_name].pop('deleted')

        for match_name, album in data_service.items():
            if match_name not in index_entry:
                index_entry[album.get_match_name()] = {
                    'indexed': album.get_modification_time()
                }

        fileref = open(self.path, 'w')
        index = {'last_update': 0, 'entry': index_entry}
        json.dump(index, fileref)

    def purge(self):
        for album in self.fetch_all():
            album.purge()
        os.remove(self.path)

    def fetch_all(self):
        data = self.fetch()
        if 'entry' in data:
            return data['entry']
        else:
            return {}

    def fetch(self):
        if not util.index.Config.Config.dir:
            return {}
        data = {}
        try:
            # create dirs
            dirs = os.path.split(self.path)[0]
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            # load json content
            if os.path.exists(self.path):
                fileref = open(self.path, 'r')
                data = json.load(fileref)
        except Exception as e:
            # todo add logger
            pass
        return data

    def fetch_all_as_album(self):
        albums = []
        for match_name in self.fetch_all():
            albums.append(self.service.Album(match_name))
        return albums

    def fetch_all_deleted(self):
        return {k: v for k, v in self.fetch_all().items() if 'deleted' in v and v['deleted']}
