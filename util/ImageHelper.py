from PIL import Image
import pyexiv2
import tempfile
import time


class ImageHelper:

    def __init__(self):
        pass

    @staticmethod
    def get_size(path):
        try:
            size = Image.open(path).size
        except IOError:
            # if this is not an image, we cannot get the size
            size = [0, 0]
        return size

    @staticmethod
    def get_exif_creation_time(path):
        try:
            metadata = pyexiv2.ImageMetadata(path)
            metadata.read()
        except IOError:
            # if this is not an image, we cannot get the size
            return 0
        if 'Exif.Photo.DateTimeOriginal' in metadata.exif_keys:
            return time.mktime(metadata['Exif.Photo.DateTimeOriginal'].value.timetuple())
        return 0

    @staticmethod
    def copy_exif(from_path, to_path):
        metadata_src = pyexiv2.ImageMetadata(from_path)
        metadata_src.read()
        metadata_target = pyexiv2.ImageMetadata(to_path)
        metadata_target.read()
        metadata_src.copy(metadata_target)
        metadata_target.write()

    # used https://github.com/jackpal/picasawebuploader/blob/master/main.py and 
    # http://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
    @staticmethod
    def resize(path, max_width, max_height):
        return_path = path

        im = Image.open(path)
        if im.size[0] <= max_width and im.size[1] <= max_height:
            return return_path

        tempfile.gettempdir()
        resize_path = tempfile.NamedTemporaryFile(delete=False, suffix='.' + im.format)
        im.thumbnail((max_width, max_height), Image.ANTIALIAS)
        im.save(resize_path, im.format)
        ImageHelper.copy_exif(path, resize_path.name)
        return resize_path.name

