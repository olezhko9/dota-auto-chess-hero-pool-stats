from PIL import Image
from dac.ocr import recognize_heroes_on_image
import os


def crop_heroes(im):
    crop_config = {
        'x': 285,
        'y': 150,
        'margin': 90,
        'w': 160,
        'h': 200,
    }

    heroes = recognize_heroes_on_image(im, show=False, need_crop=True)
    cropped_heroes = []

    if len(heroes) == 5:
        for i in range(5):
            hero_crop = im.crop((crop_config['x'] + crop_config['margin'] * (i + 1) + crop_config['w'] * i,
                                 crop_config['y'],
                                 crop_config['x'] + (crop_config['margin'] + crop_config['w']) * (i + 1),
                                 crop_config['y'] + crop_config['h']
                                 ))

            hero_crop.thumbnail((36, 40))
            cropped_heroes.append((heroes[i], hero_crop))
    return cropped_heroes


if __name__ == '__main__':
    images_path = '../../images/'
    unique_hero_img_count = 0
    for filename in os.listdir(images_path):
        filename = images_path + filename
        if os.path.isdir(filename):
            continue
        else:
            hero_crop = crop_heroes(Image.open(filename))
            for hc in hero_crop:
                hc[1].save(images_path + "heroes/" + hc[0] + " - " + str(unique_hero_img_count) + ".png")
                unique_hero_img_count += 1
