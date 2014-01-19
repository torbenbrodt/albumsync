import tempfile


class Image:

    def __init__(self):
        pass

    def copy_exif(self, fromPath, toPath):
        pass

    # used https://github.com/jackpal/picasawebuploader/blob/master/main.py and 
    # http://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
    def resize(self, path, max_width, max_height):
        returnPath = path

        im = Image.open(path)
        if (im.size[0] > max_width  or im.size[1] > max_height):
            resizePath = tempfile.NamedTemporaryFile(delete=False)
            im.thumbnail((max_width, max_height), Image.ANTIALIAS)
            im.save(resizePath, "JPEG")
            self.copyExif(path, resizePath)
            returnPath = resizePath

        return returnPath

