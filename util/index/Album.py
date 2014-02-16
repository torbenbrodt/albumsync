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
        self.path = ''
        self.index = {}
        self.synced = False
        if util.index.Config.Config.dir:
            self._load_index_from_file()

    def _load_index_from_file(self):
        self.path = os.path.join(util.index.Config.Config.dir, self.service.__name__ + '.index')
        try:
            # create dirs
            dirs = os.path.split(self.path)[0]
            if not os.path.exists(dirs):
                os.makedirs(dirs)
                # load json content
            if os.path.exists(self.path):
                fileref = open(self.path, 'r')
                self.index = json.load(fileref)
        except Exception as e:
            # todo add logger
            pass

    def sync(self, force=False):
        if not force and self.synced:
            return

        if not util.index.Config.Config.dir:
            return

        if util.index.Config.Config.ttl > 0 and 'last_update' in self.index and \
                util.index.Config.Config.ttl > time.time() - float(self.index['last_update']):
            return

        self.synced = True

        self.index['last_update'] = time.time()
        fileref = open(self.path, 'w')
        json.dump(self.index, fileref)

        # read media from service
        data_service = dict(
            (album_target.get_match_name(), album_target) for album_target in self.service.Album.Album.fetch_all())

        if 'entry' not in self.index:
            self.index['entry'] = {}

        # check existing data for deletion
        for match_name, album in self.index['entry'].items():
            if match_name not in data_service:
                self.index['entry'][match_name]['deleted'] = time.time()
            elif 'deleted' in album and album['deleted']:
                self.index['entry'][match_name].pop('deleted')

        for match_name, album in data_service.items():
            if match_name not in self.index['entry']:
                self.index['entry'][album.get_match_name()] = {
                    'indexed': album.get_modification_time(),
                    'url': album.get_url()
                }

        # write data
        self.index['last_update'] = time.time()
        fileref = open(self.path, 'w')
        json.dump(self.index, fileref)

    def purge(self):
        """remove index"""
        self.sync()
        if 'entry' not in self.index:
            return
        for album in self.index['entry']:
            album.purge()
        os.remove(self.path)

    def fetch_all_as_album(self):
        """return album objects"""
        if 'entry' not in self.index:
            return []
        albums = []
        for match_name in self.index['entry']:
            url = self.index['entry'][match_name]['url']
            albums.append(self.service.Album.Album(url))
        return albums

    def fetch_all(self):
        """return albums in index"""
        if 'entry' not in self.index:
            return {}
        return self.index['entry']

    def fetch_all_deleted(self):
        """return albums which were deleted"""
        if 'entry' not in self.index:
            return {}
        return {k: v for k, v in self.index['entry'].items() if 'deleted' in v and v['deleted']}
