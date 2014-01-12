class Album:
    "Model: common public api for all albums"

    @staticmethod
    def fetchAll(self):
        "walk the web album finding albums there"

        #todo How to list and download albums which are shared with me?
        # (api / Community search?)
        entries = []
        webAlbums = gd_client.GetUserFeed()
        for webAlbum in webAlbums.entry:
            entries.append(Album(webAlbum))
        return entries

    @staticmethod
    def create(self, album_src):
        gd_client.InsertAlbum(title=album_src.getTitle(), access='private', summary='synced from ...')

    def __init__(self, webAlbum):
        self.webAlbum = webAlbum

    def getURL(self):
        return self.webAlbum.GetPhotosUri()

    def getTitle(self):
        return self.webAlbum.title.text

    def getMatchName(self):
        "this method is used to match albums"
        return self.getTitle()

    def getNumbersOfMedias(self):
        return self.webAlbum.numberFiles.text

    def getID(self):
        return self.webAlbum.id.text

    def _getEditObject(self):
        return gd_client.GetEntry(self.getID())
