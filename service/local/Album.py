class Album:
    "Model: common public api for all albums"
    self.idprefix = 'local'

    # static access
    def fetchAll(self):
        "walk the images in homedir"
        entries = []
        for path in os.scandir(homedir):
            entries[] = Album(path)
        return entries

    def __init__(self, path):
        self.path = path

    def getURL(self):
        return self.path

    def getTitle(self):
        return strip(self.path)

    def getNumbersOfMedias(self):
        return count(scandir(path))

    def getID(self)
        return self.path

    # static access
    def create(self, album_src):
        os.mkdir(homedir + '/' + urllib.quote(album_src.getTitle()))
