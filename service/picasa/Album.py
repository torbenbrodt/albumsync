import re
from service.picasa.Client import Client
from gdata.photos.service import *
from service.abstract.AbstractAlbum import AbstractAlbum
from util.Superconfig import Superconfig
from util.Deduplicator import Deduplicator


class Album(AbstractAlbum):

    @staticmethod
    def fetch_all():
        """walk the web album finding albums there
        @rtype : list of Album
        """
        feed = Client.get_client().GetUserFeed().entry
        # picasa can have multiple albums with the same name
        # so prepend the unique id, in case of duplicate
        dedu = Deduplicator()
        return dedu.run_list(feed, lambda web_ref: Album(web_ref),
                             lambda web_ref: int(web_ref.id.text.split('/')[-1]))

    @staticmethod
    def create(album_src):
        """
        @type album_src: Album
        @param album_src: source album
        @rtype Album
        """
        web_album = Client.get_client().InsertAlbum(title=album_src.get_title(), access='private',
                                                    timestamp='%i' % int(album_src.get_creation_time() * 1000),
                                                    summary='synced from https://github.com/torbenbrodt/albumsync')
        return Album(web_album)

    def save(self):
        Client.get_client().Put(self.web_ref, self.web_ref.GetEditLink().href,
                                converter=gdata.photos.AlbumEntryFromString)

    def delete(self):
        if not Superconfig.allowdelete:
            raise Exception('delete is not allowed')
        Client.get_client().Delete(self.web_ref)

    # noinspection PyMissingConstructor
    def __init__(self, web_album):
        """
        @type web_album: gdata.photos.UserFeed or url
        @param web_album: object from the gdata api
        """
        if type(web_album) is str:
            web_album = Client.get_client().GetFeed(web_album)
        self.web_ref = web_album
        self.title = ''

    def get_url(self):
        """
        @rtype : string
        """
        return self.web_ref.GetPhotosUri()

    def set_title(self, title):
        self.title = title

    def get_title(self):
        """
        @rtype : string
        """
        if self.title:
            return self.title
        return self.web_ref.title.text

    def get_match_name(self):
        """
        this method is used to match albums
        @rtype : string
        """
        return self.get_title().lower()

    def get_number_of_media(self):
        """
        @rtype : int
        """
        return self.web_ref.numphotos.text

    def get_modification_time(self):
        """
        timestamp of last modification
        @rtype: float
        """
        return time.mktime(
            time.strptime(re.sub("\.[0-9]{3}Z$", ".000 UTC", self.web_ref.updated.text), '%Y-%m-%dT%H:%M:%S.000 %Z'))

    def get_creation_time(self):
        return time.mktime(time.localtime(int(self.web_ref.timestamp.text) / 1000))
