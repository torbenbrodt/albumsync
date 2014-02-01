import mimetypes
import tempfile
import urllib
import re
import shutil
from service.picasa.Client import Client
from gdata.photos.service import *
from util.Checksum import Checksum
from util.ImageHelper import ImageHelper
from service.abstract.AbstractMedia import AbstractMedia
from util.Superconfig import Superconfig
from util.Deduplicator import Deduplicator


class Media(AbstractMedia):
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
        @type album: AbstractAlbum
        @param album:
        @return:
        @rtype : list of Media
        """
        # todo this feed does not include foreign images (e.g. Hangout Album)
        feed = Client.get_client().GetFeed(album.get_url()).entry
        # picasa can have multiple media with the same filename in a single album
        # so prepend the unique id, in case of duplicate
        dedu = Deduplicator()
        return dedu.run_list(feed, lambda web_ref: Media(album, web_ref), lambda web_ref: int(web_ref.gphoto_id.text))

    @staticmethod
    def create(album, media_src):
        """
        @param Album album:
        @type media_src: Media
        @param media_src:
        @return: Media
        """
        mimeType = media_src.get_mime_type()

        metadata = gdata.photos.PhotoEntry()
        metadata.title = atom.Title(text=urllib.quote(media_src.get_title(), ''))
        metadata.summary = atom.Summary(text=media_src.get_description(), summary_type='text')
        metadata.checksum = gdata.photos.Checksum(text=media_src.get_hash())
        if mimeType in Media.supportedImageFormats:
            media = Client.get_client().InsertPhoto(album.webAlbum.albumUri,
                                                    metadata, media_src.get_local_url(), mimeType)
        elif mimeType in Media.supportedVideoFormats:
            if media_src.get_filesize() > Media.MAX_VIDEO_SIZE:
                raise Exception("Not uploading %s because it exceeds maximum file size" % media_src.get_url())
            media = Client.get_client().InsertVideo(album.get_url(), metadata, media_src.get_local_url(), mimeType)
        else:
            raise Exception('unsupported file extension')
        return Media(album, media)

    def __init__(self, album, web_ref):
        self.album = album
        self.web_ref = web_ref
        self.title = ''
        self.local_url = ''
        self.changed = []

    def save(self):
        # upload
        if 'blob' in self.changed:
            self.web_ref = Client.get_client().UpdatePhotoBlob(self._get_edit_object().GetEditLink().href, self.get_local_url())

        entry = Client.get_client().GetEntry(self._get_edit_object().GetEditLink().href)

        # checksum is not trustable, see http://code.google.com/p/gdata-issues/issues/detail?id=2351
        media_hash = self.get_hash()
        if 'blob' in self.changed or not media_hash:
            media_hash = Checksum.get_md5(self.get_local_url())
            entry.checksum = gdata.photos.Checksum(text=media_hash)

        if 'title' in self.changed:
            entry.title = atom.Summary(text=self.get_title(), summary_type='text')

        if 'description' in self.changed:
            entry.summary = atom.Summary(text=self.get_description(), summary_type='text')

        # It is important that you don't keep the old object around,
        # once it has been updated. See http://code.google.com/apis/gdata/reference.html#Optimistic-concurrency
        self.web_ref = Client.get_client().UpdatePhotoMetadata(entry)
        # reset changed attributes
        self.changed = []

    def _get_edit_object(self):
        if not self.web_ref.gphoto_id.text:
            raise Exception("missing gphoto_id")
        url = '/data/feed/api/user/%s/albumid/%s/photoid/%s' % (
            "default", self.web_ref.albumid.text, self.web_ref.gphoto_id.text)
        return Client.get_client().GetFeed(url)

    def get_hash(self):
        return self.web_ref.checksum.text

    def get_filesize(self):
        """in bytes"""
        return int(self.web_ref.size.text)

    def get_dimensions(self):
        """
        @rtype: list of int
        """
        return [int(self.web_ref.width.text), int(self.web_ref.height.text)]

    def get_modification_time(self):
        return time.mktime(
            time.strptime(re.sub("\.[0-9]{3}Z$", ".000 UTC", self.web_ref.updated.text), '%Y-%m-%dT%H:%M:%S.000 %Z'))

    def set_title(self, title):
        self.title = title

    def get_title(self):
        """title"""
        if self.title:
            return self.title
        assert self.web_ref.title.text, 'title is empty'
        return urllib.unquote(self.web_ref.title.text)

    def get_description(self):
        """description"""
        return self.web_ref.description.text

    def get_url(self):
        return self.web_ref.content.src

    def delete(self):
        if not Superconfig.allowdelete:
            raise Exception('delete is not allowed')
        Client.get_client().Delete(self._get_edit_object())

    def get_local_url(self):
        """this uses download"""
        if self.local_url:
            return self.local_url

        self.local_url = os.path.join(tempfile.gettempdir(), self.get_title())
        urllib.urlretrieve(self.get_url(), self.local_url)
        return self.local_url

    def get_mime_type(self):
        path = self.get_local_url()
        return mimetypes.guess_type(path)[0]

    def download(self, path):
        shutil.copyfile(self.get_local_url(), path)

    def get_match_name(self):
        """this method is used to match media"""
        return self.get_title()

    def is_resize_necessary(self):
        if self.album.web_ref.access.text == 'public':
            return False
        width, height = self.get_dimensions()
        return width > self.MAX_FREE_IMAGE_DIMENSION or height > self.MAX_FREE_IMAGE_DIMENSION

    def resize(self):
        """
        call save() afterwards!
        @return: result if image was changed
        """
        tmp = self.local_url
        self.local_url = ImageHelper.resize(self.get_local_url(),
                                            self.MAX_FREE_IMAGE_DIMENSION,
                                            self.MAX_FREE_IMAGE_DIMENSION)
        # check if the image changed
        changed = tmp != self.local_url
        if changed:
            self.changed.append('blob')
        return changed

    def __del__(self):
        # delete temporary local file if present
        if self.local_url:
            os.remove(self.local_url)

    def validate(self):
        """make this object valid
        """
        if not self.get_hash():
            self.save()