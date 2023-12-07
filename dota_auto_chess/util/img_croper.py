import os
from PIL import Image


def crop_heroes(image):
    crop_config = {
        'x': 285,
        'y': 150,
        'margin': 90,
        'w': 160,
        'h': 200,
    }

    cropped_heroes = []
    for i in range(5):
        hero_crop = image.crop((crop_config['x'] + crop_config['margin'] * (i + 1) + crop_config['w'] * i,
                                crop_config['y'],
                                crop_config['x'] + (crop_config['margin'] + crop_config['w']) * (i + 1),
                                crop_config['y'] + crop_config['h']
                                ))

        hero_crop.thumbnail((36, 40))
        cropped_heroes.append(hero_crop)

    return cropped_heroes


def crop_hero_text(image):
    # TODO: добавить поддержку разных разрешений
    crop = (360, 380, 1210, 25)
    return image[crop[1]:crop[1] + crop[3], crop[0]:crop[0] + crop[2]]


if __name__ == '__main__':
    from dota_auto_chess.ocr import heroes_on_image

    images_path = '../../images/'
    unique_hero_img_count = 0
    for filename in os.listdir(images_path):
        filename = os.path.join(images_path, filename)
        if os.path.isdir(filename):
            continue
        else:
            heroes = heroes_on_image.recognize_heroes_on_image(filename, need_crop=True, show=False)
            if len(heroes) == 5:
                hero_crop = crop_heroes(Image.open(filename))
                for idx, hero in enumerate(hero_crop):
                    hero.save(images_path + "heroes/" + heroes[idx] + " - " + str(unique_hero_img_count) + ".png")
                    unique_hero_img_count += 1
