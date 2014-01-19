import mimetypes
import tempfile
import urllib
import re
from service.picasa.Client import Client
from gdata.photos.service import *
from util.Callback import Callback


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
        @type album: Album
        @param album:
        @return:
        @rtype : list of Media
        """
        entries = []
        for web_ref in Client.get_client().GetFeed(album.get_url()).entry:
            entries.append(Media(album, web_ref))
        return entries

    @staticmethod
    def create(album, media_src):
        """
        @param Album album:
        @type media_src: Media
        @param media_src:
        @return: Media
        """
        mimeType = media_src.get_mim_type()

        metadata = gdata.photos.PhotoEntry()
        metadata.title = atom.Title(text=urllib.quote(media_src.get_title(), ''))
        metadata.summary = atom.Summary(text=media_src.get_description(), summary_type='text')
        metadata.checksum = gdata.photos.Checksum(text=media_src.get_hash())
        if mimeType in Media.supportedImageFormats:
            media = Client.get_client().InsertPhoto(album.webAlbum.albumUri, metadata, media_src.get_local_url(), mimeType)
        elif mimeType in Media.supportedVideoFormats:
            if media_src.get_size() > Media.MAX_VIDEO_SIZE:
                raise Exception("Not uploading %s because it exceeds maximum file size" % media_src.get_url())
            media = Client.get_client().InsertVideo(album.get_url(), metadata, media_src.get_local_url(), mimeType)
        else:
            raise Exception('unsupported file extension')
        return Media(album, media)

    def __init__(self, album, web_ref):
        self.album = album
        self.web_ref = web_ref

    def save(self):
        # todo more available attributes are checksum, updated, version, rights, summary
        #metadata.summary = atom.Summary(text=os.path.relpath(self.path,self.album.rootPath), summary_type='text')
        #metadata.checksum = gdata.photos.Checksum(text=self.getLocalHash())
        #entry = Client.get_client().GetEntry(self._get_edit_object().GetEditLink().href)
        #Client.get_client().UpdatePhotoMetadata(entry)
        pass

    def _get_edit_object(self):
        #It is important that you don't keep the old object around, once
        #it has been updated. See
        #http://code.google.com/apis/gdata/reference.html#Optimistic-concurrency

        if self.web_ref.gphoto_id:
            photo = Client.get_client().GetFeed('/data/feed/api/user/%s/albumid/%s/photoid/%s' % (
                "default", self.web_ref.albumid, self.web_ref.gphoto_id))
            return photo
            # FIXME throw exception
        return None

    def get_hash(self):
        if self.hash:
            return self.hash
        return str(self.web_ref.checksum.text)

    def get_size(self):
        """in bytes"""
        return int(self.web_ref.size.text)

    def get_date(self):
        return time.mktime(
            time.strptime(re.sub("\.[0-9]{3}Z$", ".000 UTC", self.web_ref.updated.text), '%Y-%m-%dT%H:%M:%S.000 %Z'))

    def get_title(self):
        """title"""

        # cleanup title
        if self.web_ref.title.text is None:
            return ''
        else:
            return urllib.unquote(self.web_ref.title.text)

    def get_description(self):
        """description"""
        return self.web_ref.description.text

    def get_url(self):
        return self.web_ref.content.src

    def delete(self):
        Client.get_client().Delete(self._get_edit_object())

    def get_local_url(self):
        """this uses download"""
        #todo deprecated?
        path = os.path.join(tempfile.gettempdir(), self.get_title())
        self.download(path)
        return path

    def get_mime_type(self):
        path = self.get_local_url()
        return mimetypes.guess_type(path)[0]

    def download(self, path):
        # todo check if create/edit times can be transferred (if this check is needed in SyncMedia)
        urllib.urlretrieve(self.get_url(), path)

    def get_match_name(self):
        """this method is used to match media"""
        return self.get_title()

    def is_resize_necessary(self):
        #todo ask album for restrictions, width + height
        #todo only resize if album is not public (picasa offers this for free)
        width = int(self.web_ref.width.text)
        height = int(self.web_ref.height.text)
        pass

    def resize(self):
        #todo ask if service provides serverside resizing (so any meta data is not lost) otherwise use util.Image.resize
        pass

    def set_hash(self, hash):
        self.hash = hash

    def callback(self, action, media_other):
        """callback will update the hash"""
        # update the hash
        if action in [Callback.CREATE, Callback.UPDATE]:
            self.set_hash(media_other.get_hash())
            self.save()
