from PIL import Image
import os
import pyexiv2
import tempfile
import unittest
import shutil
from util.ImageHelper import ImageHelper


class ImageHelperTest(unittest.TestCase):

    def test_resize(self):
        path = os.path.dirname(os.path.abspath(__file__)) + '/../data/openartproject_city_limits.jpg'
        new_path = ImageHelper.resize(path, 640, 480)
        im = Image.open(new_path)
        self.assertEquals(371, im.size[0])
        self.assertEquals(480, im.size[1])

    def test_exif(self):
        path_src = os.path.dirname(os.path.abspath(__file__)) + '/../data/openartproject_city_limits.jpg'
        # copy image to temporary image
        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        shutil.copy(path_src, tmpfile.name)
        path_src = tmpfile.name
        # copy image to temporary image
        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        shutil.copy(path_src, tmpfile.name)
        path_target = tmpfile.name
        # write some exif data
        metadata = pyexiv2.ImageMetadata(path_src)
        metadata.read()
        text = 'This is a useful comment.'
        metadata['Exif.Photo.UserComment'] = text
        metadata.write()
        self.assertEquals(1, len(metadata.exif_keys))
        # copy exif
        ImageHelper.copy_exif(path_src, path_target)
        # write some exif data
        metadata = pyexiv2.ImageMetadata(path_target)
        metadata.read()
        self.assertEquals(text, metadata['Exif.Photo.UserComment'].value)
        self.assertEquals(2, len(metadata.exif_keys))
