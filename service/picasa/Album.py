class Album:
    "Model: common public api for all albums"
    self.idprefix = 'picasa'

    # static access
    def fetchAll(self):
        "walk the web album finding albums there"
        entries = []
        webAlbums = gd_client.GetUserFeed()
        for webAlbum in webAlbums.entry:
            entries[] = Album(webAlbum)
        return entries

    def __init__(self, webAlbum):
        self.webAlbum = webAlbum
        self.title = webAlbum.title.text
        self.numphotos = webAlbum.numphotos.text
        self.photos = {}

    def getURL(self):
        return album.GetPhotosUri()

    def getTitle(self):
        return album.title.text

    def getNumbersOfMedias(self):
        return album.numberFiles.text

    def getID(self)
        return self.id_prefix + album.id.text

    def _getEditObject(self):
        return gd_client.GetEntry(self.getID())

    # static access
    def create(self, album_src):
        gd_client.InsertAlbum(title=album_src.getTitle(), access='private', summary='synced from ...')
