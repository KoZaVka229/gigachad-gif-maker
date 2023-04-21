import os
from sys import argv

from PIL import Image

from maker.framesmaker import FramesMaker


# IMAGE_PATH = os.getenv('IMAGE_PATH', argv[1])
IMAGE_PATH = 'example/gigacat.jpg'


# Получаем изображение и изменяем его размер (чем мельше картинка, тем быстрее программа)
image = Image.open(IMAGE_PATH).resize((500, 500))
# Создаем объект для создания кадров анимации и задаём размер кадров
maker = FramesMaker(image, frame_size=(300, 300))

""" Создаём кадры анимации движения от одной точки до другой """
maker.move(from_=(340, 155), to=(340, 200), camsize=(150, 150), count_frames=45)
maker.move(from_=(270, 180), to=(235, 180), camsize=(100, 100), count_frames=45)
maker.move(from_=(250, 200), to=(250, 260), camsize=0.8, count_frames=60)

# Сохраняем gif
maker.save_gif('out.gif')
# Открываем gif для просмотра
os.system(f'open out.gif')
