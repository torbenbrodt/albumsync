import calendar
import logging
import mimetypes
import tempfile
import urllib
import re
import shutil
from datetime import datetime
from service.picasa.Client import Client
from gdata.photos.service import *
from util.Mediatype import Mediatype
from util.Checksum import Checksum
from util.ImageHelper import ImageHelper
from service.abstract.AbstractMedia import AbstractMedia
from util.Superconfig import Superconfig
from util.Deduplicator import Deduplicator
from util.Duck import Duck
from service.picasa.Config import Config


class Media(AbstractMedia):
    """Model: common public api for all medias like photos and videos"""

    @staticmethod
    def fetch_all(album):
        """
        @type album: AbstractAlbum
        @param album:
        @return:
        @rtype : list of Media
        """
        # this feed does not include foreign images (e.g. Hangout Album)
        # to download full resolution images the imgmax=d is added
        feed_url = album.get_url() + '&imgmax=d'
        feed = Client.get_client().GetFeed(feed_url).entry
        # picasa can have multiple media with the same filename in a single album
        # so prepend the unique id, in case of duplicate
        dedu = Deduplicator()
        return dedu.run_list(feed, lambda web_ref: Media(album, web_ref), lambda web_ref: int(web_ref.gphoto_id.text))

    @staticmethod
    def create(album, media_src):
        """
        @type album: Album
        @param album:
        @type media_src: Media
        @param media_src:
        @return: Media
        """
        media_target = Media(album, None)
        media_target.update_blob(media_src)
        # this includes resizing
        media_target.validate()
        media_target.save()
        return media_target

    # noinspection PyMissingConstructor
    def __init__(self, album, web_ref):
        self.album = album
        self.web_ref = web_ref
        self.title = ''
        self.local_url = ''

    def _get_meta_data(self):
        meta_data = {'title': atom.Title(text=self.get_title()),
                     'summary': atom.Summary(text=self.get_description(), summary_type='text')}
        if self.get_hash():
            meta_data['checksum'] = gdata.photos.Checksum(text=self.get_hash())
        else:
            meta_data['checksum'] = gdata.photos.Checksum(text=Checksum.get_md5(self.get_local_url()))
        meta_data['timestamp'] = gdata.photos.Timestamp(text=str(int(self.get_creation_time() * 1000)))
        return meta_data

    def _build_entry(self, meta_data_data):
        is_new = int(self.web_ref.gphoto_id.text) == 0
        if is_new:
            metadata = gdata.photos.PhotoEntry()
        else:
            metadata = Client.get_client().GetEntry(self.web_ref.GetEditLink().href)
        for k, v in meta_data_data.items():
            setattr(metadata, k, v)
        return metadata

    def save(self):
        is_new = int(self.web_ref.gphoto_id.text) == 0
        meta_data_data = self._get_meta_data()

        # It is important that you don't keep the old object around, so always keep an eye on web_ref
        # once it has been updated. See http://code.google.com/apis/gdata/reference.html#Optimistic-concurrency
        media_type = Mediatype()
        if media_type.is_image(self.get_mime_type()):
            if is_new:
                self.web_ref = Client.get_client().InsertPhoto(self.album.get_url(),
                                                               self._build_entry(meta_data_data),
                                                               self.get_local_url(), self.get_mime_type())
        elif media_type.is_video(self.get_mime_type()):
            if is_new:
                if self.get_filesize() > Config.max_video_size:
                    raise Exception("Not uploading %s because it exceeds maximum file size" % self.get_local_url())
                self.web_ref = Client.get_client().InsertPhoto(self.album.get_url(),
                                                               self._build_entry(meta_data_data),
                                                               self.get_local_url(), self.get_mime_type())
            elif not self.get_url():
                if self.get_filesize() > Config.max_video_size:
                    raise Exception("Not uploading %s because it exceeds maximum file size" % self.get_local_url())
        else:
            raise Exception('unsupported file extension %s' % self.get_mime_type())

        # new entries already have meta data
        if not is_new:
            # updating blob, will delete checksum, so order is important
            if not self.get_url():
                self.web_ref = Client.get_client().UpdatePhotoBlob(self.web_ref,
                                                                   self.get_local_url(),
                                                                   self.get_mime_type())

        # InsertPhoto does not handle timestamp, so we need to update it again
        if self.web_ref.timestamp.text != meta_data_data['timestamp'].text:
            self.web_ref = Client.get_client().UpdatePhotoMetadata(self._build_entry(meta_data_data))

    def get_hash(self):
        if not self.web_ref.checksum.text:
            return ''
        return self.web_ref.checksum.text

    def get_filesize(self):
        """in bytes"""
        size_bytes = int(self.web_ref.size.text)
        # when we download picasa images they are equal
        # when we upload and download images they are 218 bytes bigger
        size_bytes -= 218
        return size_bytes

    def get_dimensions(self):
        """
        @rtype: list of int
        """
        return [int(self.web_ref.width.text), int(self.web_ref.height.text)]

    def get_creation_time(self):
        return time.mktime(time.localtime(int(self.web_ref.timestamp.text) / 1000))

    def get_modification_time(self):
        # The UTC time zone is sometimes denoted by the letter Z
        # time.mktime assumes the time is in localtime, but calendar.timegm takes utc
        return calendar.timegm(
            time.strptime(re.sub("\.([0-9]{3})Z$", ".\\1 UTC", self.web_ref.updated.text), '%Y-%m-%dT%H:%M:%S.%f %Z'))

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
        return self.web_ref.summary.text

    def get_url(self):
        return self.web_ref.content.src

    def delete(self):
        if not Superconfig.allowdelete:
            raise Exception('delete is not allowed')
        Client.get_client().Delete(self.web_ref)

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
        return self.get_title().lower()

    def is_resize_necessary(self):
        if Config.noresize:
            return False
        if self.album.web_ref.access.text == 'public':
            return False
        width, height = self.get_dimensions()
        return width > Client.MAX_FREE_IMAGE_DIMENSION or height > Client.MAX_FREE_IMAGE_DIMENSION

    def update_blob(self, media_src):
        self.local_url = media_src.get_url()

        if not self.web_ref:
            self.web_ref = Duck.create()
            self.web_ref.gphoto_id = Duck.create({'text': '0'})

        width, height = media_src.get_dimensions()
        self.web_ref.checksum = Duck.create({'text': media_src.get_hash()})
        self.web_ref.size = Duck.create({'text': str(media_src.get_filesize())})
        self.web_ref.title = Duck.create({'text': media_src.get_title()})
        self.web_ref.summary = Duck.create({'text': media_src.get_description()})
        self.web_ref.width = Duck.create({'text': str(width)})
        self.web_ref.height = Duck.create({'text': str(height)})
        # timestamp will hold the reference of the last modification time of source item
        self.web_ref.timestamp = Duck.create({'text': media_src.get_modification_time() * 1000})
        self.web_ref.updated = Duck.create(
            {'text': datetime.fromtimestamp(media_src.get_modification_time()).isoformat() + 'Z'})
        # leave this empty, as the indicator that the rawdata is new, see save() method
        self.web_ref.content = Duck.create({'src': ''})

    def resize(self):
        """
        @return: result if image was changed
        """
        new_url = ImageHelper.resize(self.get_local_url(),
                                     Client.MAX_FREE_IMAGE_DIMENSION,
                                     Client.MAX_FREE_IMAGE_DIMENSION)
        if self.get_local_url() == new_url:
            return False
        else:
            self.local_url = new_url
            width, height = ImageHelper.get_size(new_url)
            self.web_ref.width = Duck.create({'text': str(width)})
            self.web_ref.height = Duck.create({'text': str(height)})
            # leave this empty, as the indicator that the rawdata is new, see save() method
            self.web_ref.content = Duck.create({'src': ''})
            return True

    def validate(self):
        """make this object valid
        """
        changed = False
        if self.is_resize_necessary():
            changed = True
            logging.getLogger().warn('resize was necessary, do resize')
            self.resize()

        # checksum is not trustable, see http://code.google.com/p/gdata-issues/issues/detail?id=2351
        if len(self.get_hash()) != 32:
            changed = True
            logging.getLogger().warn('hash was invalid, do hash')

        return changed
