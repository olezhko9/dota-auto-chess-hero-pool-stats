import pytesseract
import cv2
import numpy as np

from dac.hero_list import all_heroes

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def recognize_heroes_on_image_file(filename, show=False):
    # x, y, w, h
    crop = (280, 365, 1350, 35)
    image = cv2.imread(filename, 3)

    # обрезаем область с именами героев
    crop_img = image[crop[1]:crop[1] + crop[3], crop[0]:crop[0] + crop[2]]

    return recognize_heroes(crop_img, show)


def recognize_heroes_on_image(image, show=False):
    image = np.array(image)
    return recognize_heroes(image, show)


def recognize_heroes(image, show):
    # насыщенные буквы на черном фоне
    retval, saturated_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)

    # переводим в оттенки серого
    grayscaled = cv2.cvtColor(saturated_image, cv2.COLOR_BGR2GRAY)

    # бинаризация изображения
    retval, bw_image = cv2.threshold(grayscaled, 20, 255, cv2.THRESH_BINARY)

    # черные буквы на белом фоне
    bw_image[bw_image == 255] = 100
    bw_image[bw_image == 0] = 255
    bw_image[bw_image == 100] = 0

    if show:
        cv2.imshow('threshold', bw_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return get_heroes_from_text(pytesseract.image_to_string(bw_image, lang='eng', config='--psm 7'))


def get_heroes_from_text(text):
    # TODO: Io распознается как lo - исправить
    hero_list = []
    for hero in all_heroes:
        hero_count = text.count(hero)
        if hero_count:
            hero_list.append((hero, hero_count))

    return hero_list
