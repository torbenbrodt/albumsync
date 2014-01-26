from PIL import Image
import tempfile


class ImageHelper:

    def __init__(self):
        pass

    @staticmethod
    def copy_exif(from_path, to_path):
        pass

    # used https://github.com/jackpal/picasawebuploader/blob/master/main.py and 
    # http://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
    @staticmethod
    def resize(path, max_width, max_height):
        return_path = path

        im = Image.open(path)
        if im.size[0] > max_width or im.size[1] > max_height:
            resize_path = tempfile.NamedTemporaryFile(delete=False)
            im.thumbnail((max_width, max_height), Image.ANTIALIAS)
            im.save(resize_path, 'JPEG')
            ImageHelper.copy_exif(path, resize_path)
            return_path = resize_path.name

        return return_path

