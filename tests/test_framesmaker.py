import os
import unittest

from PIL import Image

from maker.framesmaker import FramesMaker, BoundsException

IMAGE_PATH = 'gigachad.jpg'
OUT_PATH = 'tests/out'


class FramesMakerTest(unittest.TestCase):
    image = None

    def move(self, a, b, c):
        self.framemaker.move(a, b, c)
        self.framemaker.move(b, a, c)

    @classmethod
    def setUpClass(cls):
        cls.image = Image.open(IMAGE_PATH).resize((300, 300))

    def setUp(self):
        os.system('mkdir ' + OUT_PATH)
        self.framemaker = FramesMaker(FramesMakerTest.image, OUT_PATH)

    def tearDown(cls):
        os.system('rm -rf ' + OUT_PATH)

    def test_move_bounds_exception(self):
        with self.assertRaises(BoundsException):
            self.move((0, 0), (1, 1), (2, 2))
            self.move((74, 74), (226, 226), (150, 150))
            self.move((-1, -1), (301, 301), (2, 2))

    def test_move(self):
        self.move((75, 75), (224, 224), (150, 150))
        self.move((224, 75), (75, 224), (150, 150))
        self.move((100, 150), (150, 50), (50, 50))

    def test_make(self):
        self.framemaker.move((75, 75), (224, 75), (150, 150))
        self.framemaker.move((224, 75), (224, 224), (150, 150))
        self.framemaker.move((224, 224), (75, 224), (150, 150))
        self.framemaker.move((75, 224), (75, 75), (150, 150))
        self.framemaker.save_gif('make')
        os.system('open make.gif')


if __name__ == '__main__':
    unittest.main()
