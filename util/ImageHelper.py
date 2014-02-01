from PIL import Image
import pyexiv2
import tempfile


class ImageHelper:

    def __init__(self):
        pass

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

