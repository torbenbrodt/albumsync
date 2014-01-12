import mimetypes
import urllib
import re
from service.picasa.Client import Client
from gdata.photos.service import *


class Media:
    """Model: common public api for all medias like photos and videos"""

    MAX_VIDEO_SIZE = 1073741824
    MAX_FREE_IMAGE_DIMENSION = 2048
    supportedImageFormats = frozenset(["image/bmp", "image/gif", "image/jpeg", "image/png"])
    supportedVideoFormats = frozenset(
        ["video/3gpp", "video/avi", "video/quicktime", "video/mp4", "video/mpeg", "video/mpeg4", "video/msvideo",
         "video/x-ms-asf", "video/x-ms-wmv", "video/x-msvideo"])

    @staticmethod
    def fetch_all(album):
        """
        @param Album album:
        @return: Media[]
        """

        # bit of a hack, but can't see anything in api to do it.
        photos = Client.repeat(lambda: Client.get_client().GetFeed(album.get_url() + "&imgmax=d"),
                        "list photos in album %s" % album.get_title(), True)

        entries = {}
        for webPhoto in photos.entry:
            entries[webPhoto.title] = Media(album, webPhoto)
        return entries

    def __init__(self, album, webPhoto):
        self.album = album
        self.webPhoto = webPhoto

    def save(self):
        # todo what is needed?
        entry = Client.get_client().GetEntry(self._getEditObject().GetEditLink().href)
        self.webreference = Client.get_client().UpdatePhotoMetadata(entry)

    def _getEditObject(self):
        if self.gphoto_id:
            photo = Client.get_client().GetFeed('/data/feed/api/user/%s/albumid/%s/photoid/%s' % (
                "default", self.webPhoto.albumid, self.webPhoto.gphoto_id))
            return photo
            # FIXME throw exception
        return None

    def get_size(self):
        return int(self.webPhoto.size.text)

    def get_date(self):
        return time.mktime(
            time.strptime(re.sub("\.[0-9]{3}Z$", ".000 UTC", self.webPhoto.updated.text), '%Y-%m-%dT%H:%M:%S.000 %Z'))

    def get_checksum(self):
        return self.webPhoto.checksum.text

    def get_title(self):
        """title"""

        # cleanup title
        if self.webPhoto.title.text == None:
            return ""
        else:
            return urllib.unquote(self.webPhoto.title.text)

    def get_description(self):
        """description"""
        return self.webPhoto.description.text

    def get_url(self):
        return self.webPhoto.content.src

    def delete(self):
        Client.get_client().Delete(self._getEditObject())

    def get_local_urlk(self):
        tmp_path = '/tmp/xxx'
        self.download(tmp_path)
        return tmp_path

    def get_mim_type(self):
        path = self.get_local_urlk()
        return mimetypes.guess_type(path)[0]

    def download(self, path):
        url = self.get_url()
        urllib.urlretrieve(url, path)

    def get_match_name(self):
        """this method is used to match albums"""
        return self.get_title()

    @staticmethod
    def create(self, album, media_src):
        """
        @param Album album:
        @param media_src:
        @return: Media
        """
        mimeType = media_src.get_mim_type()
        metadata = gdata.photos.PhotoEntry()
        metadata.title = atom.Title(text=urllib.quote(media_src.get_title(), ''))
        metadata.summary = atom.Summary(text=media_src.get_description(), summary_type='text')
        metadata.checksum = gdata.photos.Checksum(text=media_src.get_checksum())
        if mimeType in self.supportedImageFormats:
            media = Client.get_client().InsertPhoto(album.webAlbum.albumUri, metadata, media_src.get_local_urlk(),
                                          media_src.get_mim_type())
        elif mimeType in self.supportedVideoFormats:
            if media_src.get_size() > self.MAX_VIDEO_SIZE:
                raise Exception("Not uploading %s because it exceeds maximum file size" % media_src.getID())
                return
            media = Client.get_client().InsertVideo(subAlbum.albumUri, metadata, self.path, mimeType)
        else: raise Exception('unsupported file extension')
        return Media(album, media)

