from PIL import Image
import os
import unittest
from util.ImageHelper import ImageHelper


class ImageHelperTest(unittest.TestCase):

    def test_resize(self):
        path = os.path.dirname(os.path.abspath(__file__)) + '/../data/openartproject_city_limits.jpg'
        new_path = ImageHelper.resize(path, 640, 480)
        im = Image.open(new_path)
        self.assertEquals(371, im.size[0])
        self.assertEquals(480, im.size[1])