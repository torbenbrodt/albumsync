from service.picasa.Client import Client


class Album:

    @staticmethod
    def fetch_all():
        """walk the web album finding albums there
        @rtype : list of Album
        """

        #todo How to list and download albums which are shared with me? Community search?
        entries = []
        for webAlbum in Client.get_client().GetUserFeed():
            entries.append(Album(webAlbum))
        return entries

    @staticmethod
    def create(album_src):
        """
        @type album_src: Album
        @param album_src: source album
        @rtype Album
        """
        Client.get_client().InsertAlbum(title=album_src.get_title(), access='private', summary='synced from ...')

    def __init__(self, webAlbum):
        self.webAlbum = webAlbum

    def get_url(self):
        """
        @rtype : string
        """
        return self.webAlbum.GetPhotosUri()

    def get_title(self):
        """
        @rtype : string
        """
        return self.webAlbum.title.text

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
        return self.webAlbum.numberFiles.text

    def _getEditObject(self):
        return Client.get_client().GetEntry(self.getID())
