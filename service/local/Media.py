import mimetypes
import os
import shutil
from util.Checksum import Checksum


class Media:
    """Model: common public api for all medias like photos and videos"""

    @staticmethod
    def fetch_all(album):
        """walk the directories
        @rtype : list of Album
        """
        entries = []
        for root, dirs, files in os.walk(album.get_url()):
            for path in files:
                #todo needs depth check
                media_path = os.path.join(root, path)
                entries.append(Media(album, media_path))
        return entries

    @staticmethod
    def create(album, media_src):
        path = os.path.join(album.get_url(), media_src.get_title())
        media_src.download(path)
        return Media(album, path)

    def __init__(self, album, path):
        self.album = album
        self.path = path
    
    def get_url(self):
        return self.path

    def get_hash(self):
        return Checksum.get_md5(self.get_url())

    def get_date(self):
        return os.path.getmtime(self.get_url())

    def get_size(self):
        return os.path.getsize(self.get_url())

    def delete(self):
        #todo is it possible to move to some trash directory
        os.remove(self.get_url())

    def get_title(self):
        return self.path

    def get_description(self):
        return self.path

    def get_mime_type(self):
        return mimetypes.guess_type(self.path)[0]

    def download(self, path):
        shutil.copyfile(self.path, path)

    def get_match_name(self):
        """this method is used to match media"""
        return self.get_title()

    def is_resize_necessary(self):
        return False

    def resize(self):
        #todo use util.Image.resize
        pass
