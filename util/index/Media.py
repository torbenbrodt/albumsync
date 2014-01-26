import os
import json
import util.index.Config


class Media:
    """Index Media"""

    def __init__(self, service, album):
        """
        @param service: AbstractAlbum
        @rtype service:
        """
        self.service = service
        self.album = album
        self.path = os.path.join(util.index.Config.Config.dir, self.service.__name__, self.album.get_match_name() + '.index')

    def update(self):
        # read media from service
        data_service = dict((media_target.get_match_name(), media_target) for media_target in self.service.Media.Media.fetch_all(self.album))
        # read existing index
        data_index = self.fetch_all()
        # check existing data for deletion
        for match_name, media in data_index.items():
            if match_name not in data_service:
                data_index[match_name]['deleted'] = True
            elif 'deleted' in media and media['deleted']:
                data_index[match_name].pop('deleted')

        for match_name, media in data_service.items():
            if match_name not in data_index:
                data_index[media.get_match_name()] = {
                    'date': media.get_date()
                }

        fileref = open(self.path, 'w')
        json.dump(data_index, fileref)

    def fetch_all(self):
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
        except Exception:
            pass
        return data

    def fetch_all_deleted(self):
        return {k: v for k, v in self.fetch_all().items() if 'deleted' in v and v['deleted']}
