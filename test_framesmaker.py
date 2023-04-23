import io
import unittest

from PIL import Image

from framesmaker import FramesMaker, BoundsException, NoFramesForGifException

IMAGE_PATH = 'example/gigacat.jpg'


class FramesMakerTest(unittest.TestCase):
    image = None

    def m(self, *args):
        self.framemaker.move(*args, count_frames=30)
        self.framemaker.move(*args, count_frames=30)

    @classmethod
    def setUpClass(cls):
        cls.image = Image.open(IMAGE_PATH).resize((300, 300))

    def setUp(self):
        self.framemaker = FramesMaker(FramesMakerTest.image)

    def test_move_bounds_exception(self):
        with self.assertRaises(BoundsException):
            self.m((0, 0), (1, 1), (2, 2))
            self.m((74, 74), (226, 226), (150, 150))
            self.m((-1, -1), (301, 301), (2, 2))

    def test_move(self):
        self.m((75, 75), (224, 224), (150, 150))
        self.m((224, 75), (75, 224), (150, 150))
        self.m((100, 150), (150, 50), (50, 50))

    def test_save_exception(self):
        with self.assertRaises(NoFramesForGifException), io.BytesIO() as buffer:
            self.framemaker.save_gif(buffer)

    def test_save(self):
        self.m((75, 75), (224, 224), (150, 150))

        with io.BytesIO() as buffer:
            self.framemaker.save_gif(buffer)


if __name__ == '__main__':
    unittest.main()
