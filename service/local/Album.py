import os
import urllib

class Album:
    "Model: common public api for all albums"

    @staticmethod
    def fetchAll(self):
        "walk the images in homedir"
        homedir = config.getHomeDir()
        entries = []
        for path in os.scandir(homedir):
            entries[] = Album(path)
        return entries

    @staticmethod
    def create(album_src):
        homedir = config.getHomeDir()
        os.mkdir(homedir + '/' + urllib.quote(album_src.getTitle()))

    def __init__(self, path):
        self.path = path

    def getURL(self):
        return self.path

    def getTitle(self):
        return strip(self.path)

    def getNumbersOfMedias(self):
        return count(os.scandir(path))

    def getID(self)
        return self.path

    def getMatchName(self):
        "this method is used to match albums"
        return self.getTitle()
