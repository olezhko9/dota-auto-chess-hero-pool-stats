import os
from dac.ocr import recognize_heroes_on_image


if __name__ == '__main__':

    heroes_in_file = {}

    for img in os.listdir('./images'):
        heroes = recognize_heroes_on_image('./images/' + img, show=False)
        print(img, heroes)
        heroes_in_file[img] = heroes

