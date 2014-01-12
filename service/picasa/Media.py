import urllib
import time
import re


class Media:
    "Model: common public api for all medias like photos and videos"

    MAX_VIDEO_SIZE = 1073741824
    MAX_FREE_IMAGE_DIMENSION = 2048
    supportedImageFormats = frozenset(["image/bmp", "image/gif", "image/jpeg", "image/png"])
    supportedVideoFormats = frozenset(
        ["video/3gpp", "video/avi", "video/quicktime", "video/mp4", "video/mpeg", "video/mpeg4", "video/msvideo",
         "video/x-ms-asf", "video/x-ms-wmv", "video/x-msvideo"])

    @staticmethod
    def fetchAll(album):
        """
        @param Album album:
        @return: Media[]
        """

        # bit of a hack, but can't see anything in api to do it.
        photos = repeat(lambda: gd_client.GetFeed(album.getURL() + "&imgmax=d"),
                        "list photos in album %s" % foundAlbum.albumName, True)

        entries = {}
        for webPhoto in photos.entry:
            entries[webPhoto.title] = Media(album, webPhoto)
        return entries

    def __init__(self, album, webPhoto):
        self.album = album
        self.webPhoto = webPhoto

    def save(self):
        # todo what is needed?
        entry = gd_client.GetEntry(self._getEditObject().GetEditLink().href)
        self.webreference = gd_client.UpdatePhotoMetadata(entry)

    def _getEditObject(self):
        if self.gphoto_id:
            photo = gd_client.GetFeed('/data/feed/api/user/%s/albumid/%s/photoid/%s' % (
                "default", self.webPhoto.albumid, self.webPhoto.gphoto_id))
            return photo
            # FIXME throw exception
        return None

    def getSize(self):
        return int(self.webPhoto.size.text)

    def getDate(self):
        return time.mktime(
            time.strptime(re.sub("\.[0-9]{3}Z$", ".000 UTC", self.webPhoto.updated.text), '%Y-%m-%dT%H:%M:%S.000 %Z'))

    def getHash(self):
        return self.webPhoto.checksum.text

    def getID(self):
        "unique identifier"
        return self.webPhoto.gphoto_id.text

    def getTitle(self):
        "title"

        # cleanup title
        if self.webPhoto.title.text == None:
            return ""
        else:
            return urllib.unquote(self.webPhoto.title.text)

    def getDescription(self):
        "description"
        return self.webPhoto.description.text

    def getURL(self):
        return self.webPhoto.content.src

    def delete(self):
        gd_client.Delete(self._getEditObject())

    def getLocalUrl(self):
        tmp_path = '/tmp/xxx'
        self.download(tmp_path)
        return tmp_path

    def getMimeType(self):
        path = self.getLocalUrl()
        return mimetypes.guess_type(path)[0]

    def download(self, path):
        url = self.getURL()
        urllib.urlretrieve(url, path)

    def getMatchName(self):
        "this method is used to match albums"
        return self.getTitle()

    @staticmethod
    def create(self, album, media_src):
        """
        @param Album album:
        @param media_src:
        @return: Media
        """
        mimeType = media_src.getMimeType()
        metadata = gdata.photos.PhotoEntry()
        metadata.title = atom.Title(text=urllib.quote(media_src.getTitle(), ''))
        metadata.summary = atom.Summary(text=media_src.getDescription(), summary_type='text')
        metadata.checksum = gdata.photos.Checksum(text=media_src.getHash())
        if mimeType in self.supportedImageFormats:
            media = gd_client.InsertPhoto(album.webAlbum.albumUri, metadata, media_src.getLocalUrl(),
                                          media_src.getMimeType())
        else
        if mimeType in self.supportedVideoFormats:
            if media_src.getSize() > self.MAX_VIDEO_SIZE:
                throw
                Exception("Not uploading %s because it exceeds maximum file size" % media_src.getID())
                return
        media = gd_client.InsertVideo(subAlbum.albumUri, metadata, self.path, mimeType)
        else Exception('unsupported file extension')
        return Media(album, media)

