from service.picasa.Client import Client
from gdata.photos.service import *
from service.abstract.AbstractAlbum import AbstractAlbum


class Album(AbstractAlbum):

    @staticmethod
    def fetch_all():
        """walk the web album finding albums there
        @rtype : list of Album
        """

        # todo How to list and download albums which are shared with me? Community search?
        # photos = gd_client.SearchCommunityPhotos('puppy', limit='10')
        entries = []
        for web_album in Client.get_client().GetUserFeed().entry:
            entries.append(Album(web_album))
        return entries

    @staticmethod
    def create(album_src):
        """
        @type album_src: Album
        @param album_src: source album
        @rtype Album
        """
        web_album = Client.get_client().InsertAlbum(title=album_src.get_title(), access='private', summary='synced from ...')
        return Album(web_album)

    def save(self):
        Client.get_client().Put(self.web_ref, self.web_ref.GetEditLink().href, converter=gdata.photos.AlbumEntryFromString)

    def delete(self):
        Client.get_client().Delete(self.web_ref)

    def __init__(self, web_album):
        """

        @type web_album: AlbumEntry
        @param web_album: object from the gdata api
        """
        self.web_ref = web_album

    def get_url(self):
        """
        @rtype : string
        """
        return self.web_ref.GetPhotosUri()

    def get_title(self):
        """
        @rtype : string
        """
        return self.web_ref.title.text

    def get_match_name(self):
        """
        this method is used to match albums
        @rtype : string
        """
        return self.get_title()

    def get_number_of_media(self):
        """
        @rtype : int
        """
        return self.web_ref.numphotos.text
