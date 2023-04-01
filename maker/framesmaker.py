from typing import Callable

import numpy as np
from PIL.Image import Image


def points_not_in_image_bounds(image: Image, camsize: np.ndarray, *points: np.ndarray) -> tuple[np.ndarray]:
    """ Проверяет, находятся ли точки в пределах изображения """

    def check(point: np.ndarray):
        p1, p2 = point - camsize / 2, point + camsize / 2
        return np.all((0 <= p1) & (p1 <= image.size) & (0 <= p2) & (p2 <= image.size))

    return tuple(point for point in points if not check(point))


class FramesMaker:
    """ Класс по созданию кадров анимации """

    def __init__(self, image: Image, frame_size: tuple[int, int] = None):
        """
        :param image: Изображение для обработки
        :param frame_size: Размер, к которому будет преводиться каждый кадр
        :raise ValueError: Папка из **out_path** не найдена
        """

        self.__image = image
        self.__frame_size = frame_size if frame_size else image.size
        self.__frames = []

    def move(self, from_: tuple[int, int], to: tuple[int, int], camsize: tuple[int, int] | float, count_frames: int):
        """
        Генерирует кадры движения от точки **from_** до точки **to**.

        :param from_: точка начала движения
        :param to: точка конца движения
        :param camsize: размер камеры или коэффициент уменьшения размера изображения
        :param count_frames: количество кадров, доступных для движения
        """

        if isinstance(camsize, float): camsize = np.array(self.__image.size) * camsize
        else: camsize = np.array(camsize)

        from_, to = np.array(from_), np.array(to)
        if 0 in camsize or np.all(from_ == to):
            return

        if errors := points_not_in_image_bounds(self.__image, camsize, from_, to):
            raise BoundsException(errors, camsize)

        step = (to - from_) / count_frames
        self.__frames += [self.__crop(from_ + step * i, camsize) for i in range(count_frames)]

    def map_frames(self, func: Callable[[int, Image], Image]):
        """ Сделать что-то с каждым кадром (например, изменить размер кадров) """

        self.__frames = [func(idx, frame) for idx, frame in enumerate(self.__frames)]

    def save_gif(self, path: str = 'out.gif', fps: int = 30, optimize=True):
        """
        Собирает все кадры в один GIF файл и сохраняет его

        :param path: Путь до выходного файла
        :param fps: frames per second для gif
        :param optimize: Оптимизровать ли gif?
        """

        frames = iter(self.__frames)
        next(frames).save(fp=path, format='GIF',
                          append_images=frames, save_all=True,
                          duration=1000 // fps, loop=0, optimize=optimize)

    def __crop(self, pos: np.ndarray[int, int], camsize: np.ndarray[int, int]) -> Image:
        start, end = pos - camsize / 2, pos + camsize / 2
        # noinspection PyTypeChecker
        image = self.__image.crop((*start, *end))
        return image.resize(self.__frame_size)


class BoundsException(Exception):
    def __init__(self, errors: tuple[np.ndarray], camsize: np.ndarray):
        super().__init__(', '.join(map(str, errors)) + f' {camsize=}')
