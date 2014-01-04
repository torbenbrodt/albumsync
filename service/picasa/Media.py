class Media:
    "Model: common public api for all medias like photos and videos"
    self.MAX_VIDEO_SIZE = 1073741824
    self.MAX_FREE_IMAGE_DIMENSION = 2048
    self.supportedImageFormats = frozenset(["image/bmp", "image/gif",  "image/jpeg",  "image/png"])
    self.supportedVideoFormats = frozenset(["video/3gpp", "video/avi", "video/quicktime", "video/mp4", "video/mpeg", "video/mpeg4", "video/msvideo", "video/x-ms-asf", "video/x-ms-wmv", "video/x-msvideo"])

    # @static access
    def fetchAll(self, album):

        # bit of a hack, but can't see anything in api to do it.
        photos = repeat(lambda: gd_client.GetFeed(album.webAlbum.GetPhotosUri()+ "&imgmax=d"),
          "list photos in album %s" % foundAlbum.albumName, True)

        webAlbum = WebAlbum(webAlbum, int(photos.total_results.text))
        foundAlbum.webAlbum.append(webAlbum)

        entries = {}
        for webPhoto in photos.entry:
            entries[photoTitle] = Media(webAlbum, webPhoto)
        return entries

    def __init__(self, album, webPhoto):
        self.album = album
        self.webAlbum = self.album.webAlbum
        self.webPhoto = webPhoto

        # cleanup title
        if self.webPhoto.title.text == None:
            self.webPhoto.title.text = ""
        else:
            self.webPhoto.title.text = urllib.unquote(photo.title.text)

        self.webreference = gd_client.UpdatePhotoMetadata(entry)
        self.webentry = gd_client.GetEntry(self._getEditObject().GetEditLink().href)

    def _getEditObject(self):
        if self.gphoto_id:
            photo = gd_client.GetFeed('/data/feed/api/user/%s/albumid/%s/photoid/%s' % ("default", self.albumid,  self.gphoto_id))
            return photo
        # FIXME throw exception
        return None

    def getSize(self):
        return int(webReference.size.text)

    def getDate(self):
        return time.mktime(time.strptime( re.sub("\.[0-9]{3}Z$",".000 UTC",webReference.updated.text),'%Y-%m-%dT%H:%M:%S.000 %Z'))

    def getHash(self):
        return webReference.checksum.text

    def getID(self):
        "unique identifier"
        return webReference.gphoto_id.text

    def getTitle(self):
        "title"
        return webReference.title.text

    def getDescription(self):
        "description"
        return webReference.description.text

    def getURL(self):
        return xx

#   def getAlbumID(self):
#       return webReference.albumid.text

    def delete(self):
        gd_client.Delete(self._getEditObject())

    def getLocalUrl(self):
        tmp_path ='/tmp/xxx'
        self.download(tmp_path)
        return tmp_path

    def getMimeType(self):
        path = self.getLocalUrl()
        return mimetypes.guess_type(path)[0]

    def download(self, path):
        url = self.webReference.content.src
        urllib.urlretrieve(url, path)

    # @static access
    def create(self, album, media_src):
        mimeType = media_src.getMimeType()
        metadata = gdata.photos.PhotoEntry()
        metadata.title = atom.Title(text = urllib.quote(media_src.getTitle(), ''))
        metadata.summary = atom.Summary(text = media_src.getDescription(), summary_type = 'text')
        metadata.checksum = gdata.photos.Checksum(text=media_src.getHash())
        if mimeType in supportedImageFormats:
            media = gd_client.InsertPhoto(album.webAlbum.albumUri, metadata, media_src.getLocalUrl(), media_src.getMimeType())
        else if mimeType in supportedVideoFormats:
            if media_src.getSize() > self.MAX_VIDEO_SIZE:
                throw Exception("Not uploading %s because it exceeds maximum file size" % media_src.getID())
                return  
          media = gd_client.InsertVideo(subAlbum.albumUri, metadata, self.path, mimeType) 
        else
            throw Exception('unsupported file extension')
        return Media(album, media)

