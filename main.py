import pytesseract
import cv2
import os
from dac_heroes.list import all_heroes

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def recognize_heroes_text_on_image(image_path, show=False):
    # x, y, w, h
    crop = (280, 365, 1350, 35)
    image = cv2.imread(image_path)

    # обрезаем область с именами героев
    crop_img = image[crop[1]:crop[1] + crop[3], crop[0]:crop[0] + crop[2]]

    # насыщенные буквы на черном фоне
    retval, saturated_image = cv2.threshold(crop_img, 150, 255, cv2.THRESH_BINARY)

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

    return pytesseract.image_to_string(bw_image, lang='eng', config='--psm 7')


def get_heroes_from_text(text):
    # TODO: Io распознается как lo - исправить
    hero_list = []
    for hero in all_heroes:
        hero_count = text.count(hero)
        if hero_count:
            hero_list.append((hero, hero_count))

    return hero_list


if __name__ == '__main__':

    heroes_in_file = {}

    for img in os.listdir('./images'):
        text = recognize_heroes_text_on_image('./images/' + img, show=False)
        print(img, text)
        print()
        heroes = get_heroes_from_text(text)
        heroes_in_file[img] = heroes

    for file, heroes in heroes_in_file.items():
        print(file, heroes)

