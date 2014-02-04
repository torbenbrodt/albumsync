class Mediatype:
    IMAGE_FORMATS = frozenset(["image/bmp", "image/gif", "image/jpeg", "image/png"])
    VIDEO_FORMATS = frozenset(
        ["video/3gpp", "video/avi", "video/quicktime", "video/mp4", "video/mpeg", "video/mpeg4", "video/msvideo",
         "video/x-ms-asf", "video/x-ms-wmv", "video/x-msvideo"])

    def __init__(self):
        pass

    def is_image(self, mime_type):
        return mime_type in Mediatype.IMAGE_FORMATS

    def is_video(self, mime_type):
        return mime_type in Mediatype.VIDEO_FORMATS