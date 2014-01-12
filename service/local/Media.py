import hashlib
import mimetypes
import os
import urllib


class Media:
    "Model: common public api for all medias like photos and videos"

    @staticmethod
    def fetchAll(self, album):
        entries = {}
        for path in os.scandir(album.getLocalPath()):
            entries[photoTitle] = Media(webAlbum, path)
        return entries

    @staticmethod
    def create(self, album, media_src):
        path = album.getLocalURL() + '/' + urllib.quote(media_src.get_title(), '')
        self.download(media_src.get_url(), album.getLocalURL() + '/' + urllib.quote(media_src.get_title(), ''))
        return Media(album, path)

    def __init__(self, album, path):
        self.album = album
        self.path = path
    
    def getLocalUrl(self):
        return self.path

    def getHash(self):
        md5 = hashlib.md5()
        with open(self.getLocalUrl(),'rb') as f: 
            for chunk in iter(lambda: f.read(128*md5.block_size), b''): 
                 md5.update(chunk)
        return md5.hexdigest()

    def getDate(self):
        return os.path.getmtime(self.getLocalUrl())

    def getSize(self):
        return os.path.getsize(self.getLocalUrl())

    def delete(self):
        os.remove(self.getLocalUrl())

    def getTitle(self):
        "title"
        return self.path

    def getDescription(self):
        "description"
        return self.path

    def getURL(self):
        return self.path

    def getLocalUrl(self):
        return self.path

    def getMimeType(self):
        return mimetypes.guess_type(self.path)[0]

    def download(self, path):
        os.copy(self.path, path)

    def getMatchName(self):
        "this method is used to match albums"
        return self.getTitle()
